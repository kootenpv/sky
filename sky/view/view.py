#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tornado.web
import tornado.autoreload
import tornado

import os
import shutil

from sky.crawler import crawl
from sky.crawler.crawling import get_image_set
from sky.configs import DEFAULT_CRAWL_CONFIG
from sky.helper import extractDomain
from sky.scraper import Scraper

import json
# from textblob import TextBlob


def is_numeric(x):
    try:
        int(x)
        return True
    except ValueError:
        return False


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('page_template.html', items=[], cached=False)

    def post(self):
        CRAWL_CONFIG = DEFAULT_CRAWL_CONFIG
        CRAWL_CONFIG.update({
            'collections_path': os.path.join(os.path.expanduser('~'), 'sky_view_collections/'),
            # 'max_workers': 10,
        })
        args = self.request.arguments
        print(args)
        for arg in args:
            value = args[arg][0].decode('utf8')
            if value and arg != 'url' and arg != 'checkboxcache':
                print('pre', arg, CRAWL_CONFIG[arg])
                if isinstance(CRAWL_CONFIG[arg], list):
                    CRAWL_CONFIG[arg] = [int(value)] if is_numeric(value) else [value]
                else:
                    CRAWL_CONFIG[arg] = int(value) if is_numeric(value) else value
                print('post', arg, CRAWL_CONFIG[arg])

        url = self.get_argument('url', '')

        use_cache = self.get_argument('checkboxcache', '')

        domain = extractDomain(url)
        CRAWL_CONFIG['seed_urls'] = [url]
        CRAWL_CONFIG['collection_name'] = domain[7:]

        if use_cache != 'on':

            col_path = os.path.join(CRAWL_CONFIG['collections_path'],
                                    CRAWL_CONFIG['collection_name'])
            print(col_path)
            if os.path.exists(col_path):
                shutil.rmtree(col_path)

            crawl.start(CRAWL_CONFIG)

        SCRAPE_CONFIG = CRAWL_CONFIG.copy()

        SCRAPE_CONFIG.update({
            'template_proportion': 0.4,
            'max_templates': 100
        })

        skindex = Scraper(SCRAPE_CONFIG)

        skindex.load_local_pages()
        skindex.add_template_elements()

        res = skindex.process_all(remove_visuals=True,
                                  maxn=CRAWL_CONFIG['max_saved_responses'])

        items = []
        for num, url in enumerate(res):
            if num == CRAWL_CONFIG['max_saved_responses']:
                break
            dc = res[url]
            dc['url'] = url
            dc['source_name'] = domain
            dc['images'] = [x for x in reversed(dc['images'][:5])]
            # dc['blobs'] = [TextBlob(x) for x in dc['body'] if dc['body']]
            items.append(dc)

        # this is quite out of place like this
        print('num unique images', len(get_image_set({x['url']: x for x in items})))

        if items and 'money' in items[0]:
            items = sorted(items, key=lambda x: len(x['money']), reverse=True)

        self.render('page_template.html', items=items, cached=False)

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'static')
}


def main(host='localhost', port=7900):
    # to run the server, type-in $ python view.py

    application = tornado.web.Application([
        (r"/", MainHandler),
    ], **settings)

    application.listen(int(port), host)

    ioloop = tornado.ioloop.IOLoop().instance()

    print('serving skyViewer at "{}:{}" from file: {}'.format(host, port, __file__))

    ioloop.start()

if __name__ == '__main__':
    main()
