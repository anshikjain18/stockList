from enum import Enum


class Exchanges(Enum):
    NSE = 'NSE'
    BSE = 'BSE'


class Instruments(Enum):
    Index = 'INDEX'
    BSE_equity = 'A'
    BSE_delivery_equity = 'T'
    BSE_other_equity = 'B'
    BSE_ETF = 'E'
    NSE_equity = 'EQ'
    NSE_delivery_equity = 'BE'
    NSE_gold_bonds = 'GB'
    NSE_mutual_fund = 'MF'
    NSE_delivery_mutual_fund = 'ME'
