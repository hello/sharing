# -*- coding: utf-8 -*-
#!/usr/bin/env python
from flask import *
from flask.ext.assets import Environment, Bundle
from flask.ext.babel import Babel, lazy_gettext
from flask.ext.compress import Compress
from flask.ext.session import Session

from flask_sslify import SSLify
#from flask_sitemap import Sitemap

from datetime import date, datetime

import os
import time
import utils
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

from bugsnag.flask import handle_exceptions

logging.config.fileConfig('logging.ini')
logger = logging.getLogger(__name__)

application = Flask(__name__)
application.config.from_object('config')
Session(application)
sslify = SSLify(application)
babel = Babel(application)
Compress(application)
#Sitemap(application)
handle_exceptions(application)

assets = Environment(application)
assets.url_expire = False

js = Bundle(
    Bundle(
        #'js/scrollmagic/ScrollMagic.min.js',
        #'js/scrollmagic/TweenMax.min.js',
        #'js/scrollmagic/plugins/animation.gsap.js',
    ),
    Bundle(
        'js/jquery-2.1.1.js',
        'js/modernizr.js',
        'js/retina.js',
        #'js/app.js',
    ),
    Bundle(
        #'js/modal.js',
	    #'js/modal/modal-html5video.js',
	    #'js/modal/modal-maxwidth.js',
	    #'js/modal/modal-resize.js',
    ),
    Bundle(
        'http://js.maxmind.com/js/apis/geoip2/v2.1/geoip2.js',
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

application.jinja_env.globals['year'] = date.today().year
application.jinja_env.globals['root_domain'] = os.getenv('ROOT_DOMAIN')

"""@application.before_request
def before_request():
    session.permanent = True

    if 'uuid' not in session:
        session['uuid'] = uuid.uuid4()

    if not hasattr(g, 'uuid'):
        g.uuid = session['uuid']

    application.jinja_env.globals['uuid'] = session['uuid']"""

@application.route('/dump_session', methods=['GET'])
def dump_session():
    resp = jsonify(session)
    return resp

@application.route('/robots.txt', methods=['GET'])
def robots():
    response = make_response(open('static/robots.txt').read())
    response.headers['Content-type'] = 'text/plain'
    return response

@application.route('/favicon.ico', methods=['GET'])
def favicon():
    response = make_response(open('static/img/favicon.png').read())
    response.headers['Content-type'] = 'image/x-icon'
    return response

@application.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({'status': 200})

@application.route('/dynamo/<uuid>')
def dynamo(uuid):
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('sharing')
    response = table.get_item(Key={'uuid': uuid})




    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response)

    item = response['Item']
    page = item['share_type']
    #print(item)

    import json
    import arrow
    import markdown

    md = markdown.Markdown()


    payload = json.loads(item['payload'])
    message = md.convert(payload['message'])

    table = dynamodb.Table('prod_profile_photo')
    response = table.get_item(Key={'account_id': payload['account_id']})
    photo = response['Item']['density_extra_high']

    print '***'
    pp.pprint(response)

    timestamp = arrow.Arrow.fromtimestamp(str(payload['timestamp'])[:-3])



    """return jsonify({
        'item': item['share_type'],
        'name': item['name'],
        'time': timestamp.format('MMMM DD, YYYY')
    })"""

    html = render_template(
        page + '.htm',
        page=page,
        name=item['name'],
        time=timestamp.format('MMMM DD, YYYY'),
        title=payload['title'],
        message=message,
        message_stripped=strip_tags(message),
        content=message,
        content_stripped=strip_tags(message),
        category=payload['category_name'],
        hero=payload['image'],
        photo=photo,
        uuid=uuid
    )
    return templates.prepare_template(html)


@application.route('/', defaults={'path': 'home'})
@application.route('/<path:path>')
def default(path):
    html = render_template(path + '.htm', page=path)
    return templates.prepare_template(html)
    #abort(404)

def strip_tags(raw_html, length=200):
    cleanr = re.compile('<.*?>')
    cleaned = re.sub(cleanr,'', raw_html).replace('\n', '')

    return cleaned[:length] + (cleaned[length:] and '...')

if __name__ == '__main__':
    logger.debug("Time is: %s", int(time.time() * 1000))
    application.run(host='0.0.0.0')
