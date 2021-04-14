# from geopy.geocoders import Nominatim
# geolocator = Nominatim(user_agent="ussbot")
# location = geolocator.geocode("175 5th Avenue NYC")
# print(location.address)




"""
user naver cloud geolocation service
"""

import requests
import time
import sys
import os
import hashlib
import hmac
import base64
import json
from datetime import datetime
import argparse


# Signature Make
def make_signature(method, basestring, timestamp, access_key, secret_key):
    secret_key = bytes(secret_key, 'UTF-8')
    message = method + " " + basestring + "\n" + timestamp + "\n" + access_key
    message = bytes(message, 'UTF-8')
    signature = base64.b64encode(hmac.new(secret_key, message, digestmod=hashlib.sha256).digest())
    return signature


def requestApi(timestamp, access_key, signature, uri):
    
    # Header for Request
    headers = {'x-ncp-apigw-timestamp': timestamp,
               'x-ncp-iam-access-key': access_key,
               'x-ncp-apigw-signature-v2': signature}

    # Geolocation API Request
    res = requests.get(uri, headers=headers)

    # Check Response
    print('status : %d' % res.status_code)
    print('content : %s' % res.content)


def main():
    
    # Signature 생성에 필요한 항목
    method = "GET"
    IP_ADDRESSS = "YOURIP"
    basestring = f"/geolocation/v2/geoLocation?ip={IP_ADDRESSS}&ext=t&responseFormatType=json"
    timestamp = str(int(time.time() * 1000))
    access_key = "YOUR_ACCESS_KEY"  # access key id (from portal or sub account)
    secret_key = "YOUR_SECRET_KEY"  # secret key (from portal or sub account)
    signature = make_signature(method, basestring, timestamp, access_key, secret_key)
    
    # GET Request
    hostname = "https://geolocation.apigw.ntruss.com"
    requestUri = hostname + basestring
    requestApi(timestamp, access_key, signature, requestUri)

if __name__ == "__main__":
    main()
    
    