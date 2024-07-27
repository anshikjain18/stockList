#!/bin/bash

# copying the environment file to the directory
cp ../.env .

cd stockListBackend

# activating python virtual environment
source stockList/bin/activate

# installing python dependencies
pip install -r requirements.txt

# running backend
python3 main.py

cd ../stockListUI

# installing npm dependencies
npm install

# running UI
ng build
