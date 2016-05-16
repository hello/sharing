import Cookie
import datetime
import random
import logging
import os

logger = logging.getLogger(__name__)

def set_referrer(referrer):
   expiration = datetime.datetime.now() + datetime.timedelta(days=30)
   cookie = Cookie.SimpleCookie()
   cookie["referrer"] = random.randint(1000000000, 10000000000)
   cookie["referrer"]["domain"] = "." + os.getenv('ROOT_DOMAIN')
   cookie["referrer"]["path"] = "/"
   cookie["referrer"]["expires"] = \
      expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
   return cookie.output()

def get_referrer():
   try:
      cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])
      return cookie["referrer"].value
   except (Cookie.CookieError, KeyError):
      # No cookie
      return False
