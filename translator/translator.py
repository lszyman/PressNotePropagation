# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import websocket
import thread
import json
import requests
import urllib
import wave
import audioop
from time import sleep
import StringIO
import struct
import sys
import codecs
from xml.etree import ElementTree


def get_token():
    #Get the access token from ADM, token is good for 10 minutes
    urlArgs = {
        'client_id': os.environ.get('CLIENT_ID'),
        'client_secret': os.environ.get('CLIENT_SECRET'),
        'scope': 'http://api.microsofttranslator.com',
        'grant_type': 'client_credentials'
    }
    oauthUrl = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
    try:
        oauthToken = json.loads(requests.post(oauthUrl, data = urllib.urlencode(urlArgs)).content) #make call to get ADM token and parse json
        finalToken = "Bearer " + oauthToken['access_token']
    except OSError:
        pass
    return finalToken

def translate(input_string, token, lang_in = 'es', lang_out = 'en'):
    headers = {"Authorization ": token}
    translateUrl = "http://api.microsofttranslator.com/v2/Http.svc/Translate?text={}&from={}&to={}".format(input_string, lang_in, lang_out)
    try:
        translationData = requests.get(translateUrl, headers = headers) #make request
        translation = ElementTree.fromstring(translationData.text.encode('utf-8')) # parse xml return values
        return translation.text
    except OSError:
        print "Error while translating"



def find_dirs_without_translation(input_dir):
    data_without_translation = []

    for root, dirs, files in os.walk(input_dir):
        last_dir = root.split('/')[-1]
        if last_dir.startswith('es_') or last_dir.startswith('fr_'):
            if 'rss.csv' in files and 'rss_en.csv' not in files:
                data_without_translation.append((root, last_dir[:2]))
    return data_without_translation

def translate_notes_list(notes_list, lang_in = "es", lang_out = "en"):
    token = get_token()
    for note in notes_list:
        note.title = translate(note.title, token, lang_in, lang_out)
        note.text = translate(note.text, token, lang_in, lang_out)
    return notes_list

def main():
    token = get_token()
    print translate("thank you", token, 'en', 'pl')

if __name__ == '__main__':
    if len(sys.argv) == 2:
        input_dir = sys.argv[1]
        main(input_dir)
    else:
        print "Usage:"
        print "  python -m translator.translator [input_dir]"
        print "  eg. python -m translator.translator geomedia"
