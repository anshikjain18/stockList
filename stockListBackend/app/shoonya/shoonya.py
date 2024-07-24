import json
import os
import zipfile
import pandas as pd
import requests
import logging
from datetime import datetime
from app.dao.shoonya import Shoonya
from app.enums import Exchanges, Instruments
from app.models import Symbols

logger = logging.getLogger(__name__)
root = 'https://api.shoonya.com/'
masters = ['NSE_symbols.txt.zip', 'BSE_symbols.txt.zip']


def get_exchange_instruments(zip_file):
    try:
        logger.info(f'downloading {zip_file}')
        r = requests.get(root + zip_file, allow_redirects=True)
        open(zip_file, 'wb').write(r.content)
    except Exception as e:
        logger.error(f"Unable to get zips from Shoonya, error - {e}")
    try:
        with zipfile.ZipFile(zip_file) as z:
            z.extractall()
        os.remove(zip_file)
        logger.info(f'removed: {zip_file}')
    except Exception as e :
        logger.error(f"Invalid file error - {e}")


def get_relevant_data(filename):
    try:
        data = pd.read_csv(filename)
        data = data[data.columns[:-1]]
        valid_instruments = [str(instrument.value) for instrument in Instruments]
        return data[data['Instrument'].isin(valid_instruments)]
    except FileNotFoundError:
        logger.error(f"Error: File {filename} not found.")
    except pd.errors.ParserError as e:
        logger.error(f"Error parsing CSV data: {e}")


def set_symbols_in_db(data):
    for index, row in data.iterrows():
        try:
            exchange = Exchanges[row['Exchange']].value
            token = int(row['Token'])
            lot_size = int(row['LotSize'])
            symbol = row['Symbol']
            trading_symbol = row['TradingSymbol']
            instrument = row['Instrument']
            tick_size = float(row['TickSize'])

            symbol_object = Symbols(
                exchange=exchange,
                token=token,
                lot_size=lot_size,
                symbol=symbol,
                trading_symbol=trading_symbol,
                instrument=instrument,
                tick_size=tick_size
            )
            symbol_object.save()
        except (ValueError, KeyError) as e:
            logger.error(f"Error creating object for row {index + 1} -> {row}: {e}. Skipping row.")


def remove_symbol_files(filename):
    os.remove(filename)
    logger.info(f'removed: {filename}')


def update_symbols():
    logger.info(f"Deleted {Symbols.objects.delete()} symbols.")
    for zip_file in masters:
        get_exchange_instruments(zip_file)
        filename = zip_file[:-4]
        data = get_relevant_data(filename)
        set_symbols_in_db(data)
        remove_symbol_files(filename)


def update_closing_prices():
    shoonya_client = Shoonya()
    for symbol in Symbols.objects:
        date = datetime.utcnow().replace(hour=9, minute=15, second=0, microsecond=0)
        start_time = str(int(date.timestamp()))
        end_time = str(int(date.replace(hour=23, minute=59, second=59).timestamp()))
        try:
            response = shoonya_client.tp_series(symbol.exchange.value, str(symbol.token), start_time, end_time,
                                            json.loads(shoonya_client.response.text).get('susertoken'))

            if len(json.loads(response.text)) != 3:
                symbol.prev_closing_price = json.loads(response.text)[0].get("intc")
                symbol.prev_closing = datetime.fromtimestamp(float(json.loads(response.text)[0].get("ssboe")))
                symbol.save()
            else:
                logger.warning(f"Error fetching closing prices for symbol {symbol.symbol}, error -"
                               f"{json.loads(response.text)}")
                continue
        except Exception as e:
            logger.error(f"Error fetching closing prices, error - {e}")
