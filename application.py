# -*- coding: utf-8 -*-
#!/usr/bin/env python
from flask import *
from flask.ext.assets import Environment, Bundle
from flask.ext.babel import Babel, lazy_gettext
from flask.ext.compress import Compress
#from flask.ext.session import Session

from flask_sslify import SSLify

from datetime import date, datetime

import os
import time
import logging
import logging.config
import re
import hashlib
import uuid

import templates

import pylibmc
import bugsnag
import boto3
import re
import json
import markdown

from bugsnag.flask import handle_exceptions

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)

application = Flask(__name__)
application.config.from_object('config')
#Session(application)
sslify = SSLify(application)
babel = Babel(application)
Compress(application)
handle_exceptions(application)

assets = Environment(application)
assets.url_expire = False

js = Bundle(
    Bundle(
        'js/jquery-2.1.1.js',
        'js/modernizr.js',
        'js/retina.js',
        'js/app.js',
    ),
    Bundle(
        'js/modal.js',
	    'js/modal/modal-html5video.js',
	    'js/modal/modal-maxwidth.js',
	    'js/modal/modal-resize.js',
    ),
    filters='jsmin',
    output='js/compiled.js'
)

css = Bundle(
    'css/grids-responsive-min-0.5.0.css',
    'css/base.css',
    filters='cssmin',
    output='css/compiled.css'
)

assets.register('js_all', js)
assets.register('css_all', css)

if os.getenv('APP_DEBUG'):
    application.jinja_env.globals['debug'] = True
application.jinja_env.globals['year'] = date.today().year
application.jinja_env.globals['root_domain'] = os.getenv('ROOT_DOMAIN')

@application.before_request
def before_request():
    session.permanent = True

    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4()

    if not hasattr(g, 'uuid'):
        g.uuid = session['uuid']

    application.jinja_env.globals['uuid'] = session['uuid']

@application.route('/dump_session', methods=['GET'])
def dump_session():
    return jsonify(session)

@application.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 200})

@application.route('/robots.txt', methods=['GET'])
def robots():
    return send_file('static/robots.txt', mimetype='text/plain')

@application.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_file('static/img/favicon.png', mimetype='image/x-icon')

@application.route('/trend/<uuid>')
def trend(uuid):
    return templates.trend()

@application.route('/insight/<uuid>')
def insight(uuid):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('sharing')
    response = table.get_item(Key={'uuid': uuid})

    insight = response['Item']
    payload = json.loads(insight['payload'])

    table = dynamodb.Table('prod_profile_photo')
    response = table.get_item(Key={'account_id': insight['account_id']})

    photo = ''

    if 'Item' in response:
        photo = response['Item']['density_extra_high']

    content = {}

    if 'info' in insight:
        content = json.loads(insight['info'])
    return templates.insight(insight, payload, content, photo, uuid)

@application.route('/')
def default():
    return redirect('https://hello.is/', code=302)

if __name__ == '__main__':
    logger.debug("Time is: %s", int(time.time() * 1000))
    application.run(host='0.0.0.0')
