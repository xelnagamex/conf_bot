#!/usr/bin/python3
# -*- coding: utf-8 -*-
from webhook import WebHook
import settings
import signal
import sys

# catch ctrl+c 
def signal_handler(signal, frame):
        print('Exiting...')
        settings.db.close()
        sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

wh = WebHook(
    certfile = 'assets/cert.pem',
    keyfile='assets/cert.key',
    port=8443)

wh.serve()
