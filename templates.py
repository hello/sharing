from flask import render_template

import re
import os
import hashlib
import markdown

import arrow

def insight(item, payload, content, photo, uuid):
    md = markdown.Markdown()
    timestamp = arrow.Arrow.fromtimestamp(str(payload['timestamp'])[:-3])

    html = render_template(
        'insight.htm',
        page='insight',
        name=item['name'],
        time=timestamp.format('MMMM DD, YYYY'),
        title=payload['title'],
        subtitle=content['title'],
        message=md.convert(payload['message']),
        message_stripped=strip_tags(md.convert(payload['message'])),
        content=md.convert(content['text']),
        content_stripped=strip_tags(md.convert(content['text'])),
        category=payload['category_name'],
        hero=payload['image'],
        photo=photo,
        uuid=uuid
    )
    return prepare_template(html)

def strip_tags(raw_html, length=200):
    cleanr = re.compile('<.*?>')
    cleaned = re.sub(cleanr,'', raw_html).replace('\n', '')

def prepare_template(html):
    #html = html.replace('https://s3.amazonaws.com/hello-accounts', '//d1hlomd23snoaq.cloudfront.net')
    #html = html.replace('https://s3.amazonaws.com/hello-data', '//d20cc2y87juqnq.cloudfront.net')
    html = html.replace('https://s3.amazonaws.com/hello-accounts', '//accounts.hellocdn.net')
    html = html.replace('https://s3.amazonaws.com/hello-data', '//data.hellocdn.net')

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

        new_url = '//' + os.getenv('ROOT_CDN') + '/' + hashlib.md5(('sharing' + str(version) + asset).encode('utf-8')).hexdigest() + retina + '.' + ext
        html = html.replace(url, new_url)

        if (new_url + '" data-no-retina' not in html) and ext in ('jpg', 'jpeg', 'png'):
            retina_url = new_url.replace('.' + ext, '@2x.' + ext)
            html = html.replace('src="' + new_url, 'src="' + new_url + '" data-at2x="' + retina_url)
    return '' . join(line.strip() for line in html.split("\n"))
