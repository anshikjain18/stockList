#!/bin/bash

# copying the environment file to the directory
cp ../.env stockListBackend/

# edit the mongodb URI
sed -i 's/\\//g' stockListBackend/.env

cd stockListBackend

# activating python virtual environment
python3 -m venv stockList
source stockList/bin/activate

# installing python dependencies
pip install -r requirements.txt

# running backend
python3 main.py