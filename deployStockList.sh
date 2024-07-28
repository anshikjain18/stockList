#!/bin/bash

# copying the environment file to the directory
cp ../.env .

# edit the mongodb URI
sed -i 's/\\//g' .env

cd stockListBackend

# activating python virtual environment
python3 -m venv stockList
source stockList/bin/activate

# installing python dependencies
pip install -r requirements.txt

cd ../stockListUI

# installing npm dependencies
npm install
