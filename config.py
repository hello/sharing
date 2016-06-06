# -*- coding: utf-8 -*-
import os
import pylibmc
import logging

if os.getenv('SHARING_APP_DEBUG'):
    logging.debug('Debug mode')

    DEBUG = True
else:
    DEBUG = False
    #SESSION_COOKIE_DOMAIN = 'hello.is'

SSLIFY_SKIPS = ['healthcheck']
SECRET_KEY = os.getenv('SHARING_APP_SECRET_KEY')
SESSION_COOKIE_NAME = 'hello_session'
SESSION_COOKIE_PATH	= '/'
#SESSION_TYPE = 'memcached'
SESSION_PERMANENT = True
SESSION_COOKIE_HTTPONLY = False
SESSION_USE_SIGNER = True
PERMANENT_SESSION_LIFETIME = 31536000
#SESSION_MEMCACHED = pylibmc.Client([os.getenv('MEMCACHED_HOSTNAME')], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})


LANGUAGES = {
  'en-US': 'English',
}
