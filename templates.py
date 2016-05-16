from flask import render_template

import re
import os
import hashlib

def prepare_template(html):
    if os.getenv('SHARING_APP_DEBUG'):
        return html

    assets = re.findall('/static/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', html)

    file = open('static/s3deploy.txt', 'r')
    version = file.read()

    html = html.replace('content="https://' + os.getenv('ROOT_DOMAIN') + '/static/', 'content="https:/static/')
    html = html.replace('rel="image_src" href="https://' + os.getenv('ROOT_DOMAIN') + '/static/', 'rel="image_src" href="https:/static/')

    for url in assets:
        asset = url.replace('/static/', '')
        ext = url.split('.')[-1]
        retina = ''

        if '@' in url and 'x.' in url:
            retina = url.split('@')[1].split('x')[0]
            url = url.replace('@' + retina + 'x', '')
            retina = '@' + retina + 'x'

        new_url = '//' + os.getenv('ROOT_CDN') + '/' + hashlib.md5('marketing' + str(version) + asset).hexdigest() + retina + '.' + ext
        html = html.replace(url, new_url)

        if (new_url + '" data-no-retina' not in html) and ext in ('jpg', 'jpeg', 'png'):
            retina_url = new_url.replace('.' + ext, '@2x.' + ext)
            html = html.replace('src="' + new_url, 'src="' + new_url + '" data-at2x="' + retina_url)
    return '' . join(line.strip() for line in html.split("\n"))
