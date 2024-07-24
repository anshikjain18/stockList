import json
import os
import pyotp
import requests
import logging

logger = logging.getLogger(__name__)


class Shoonya:
    headers = {"Content-Type": "application/json"}
    def __init__(self):
        totp = pyotp.parse_uri(os.getenv('SHOONYA_TOTP_URI')).now()
        creds = {
            "apkversion": "1.0.15",
            "uid": os.getenv('SHOONYA_UID'),
            "pwd": os.getenv('SHOONYA_PWD'),
            "factor2": f"{totp}",
            "vc": os.getenv('SHOONYA_VC'),
            "appkey": os.getenv('SHOONYA_APP_KEY'),
            "imei": os.getenv('SHOONYA_IMEI'),
            "source": "API"
        }
        self.response = requests.post(os.getenv('SHOONYA_HOST') + "/QuickAuth", self.generate_shoonya_payload(creds),
                                      self.headers)
        logger.info("Shoonya client initialized.")


    @staticmethod
    def generate_shoonya_payload(json_payload, jkey=None):
        payload = f'jData={json.dumps(json_payload)}'
        return payload + f'&jKey={jkey}' if jkey else payload


    def tp_series(self, exch, token, st, et, jkey):
        payload = {
            "uid": os.getenv('SHOONYA_UID'),
            "exch": exch,
            "token": token,
            "st": st,
            "et": et
        }
        logger.debug(f"Sending post request for token - {token} and exchange - {exch}")
        return requests.post(os.getenv('SHOONYA_HOST') + "/TPSeries", self.generate_shoonya_payload(payload, jkey),
                             self.headers)
