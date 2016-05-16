# -*- coding: utf-8 -*-
import os
import pylibmc
import logging

if os.getenv('SHARING_APP_DEBUG'):
    logging.debug('Debug mode')

    DEBUG = True
else:
    DEBUG = False
    SESSION_COOKIE_DOMAIN = 'hello.is'

SSLIFY_SKIPS = ['healthcheck']

LANGUAGES = {
  'en-US': 'English',
}
