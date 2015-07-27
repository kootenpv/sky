#!/usr/bin/env python3.4

"""A simple web crawler -- main driver program."""

import asyncio
import logging
import sys

from .crawling import Crawler
from .reporting import report
import os

def get_loop(select = False):
    if os.name == 'nt':
        from asyncio.windows_events import ProactorEventLoop
        loop = ProactorEventLoop()
    elif select:
        loop = asyncio.SelectorEventLoop()
    else:
        loop = asyncio.get_event_loop()
    return loop

def get_crawler_from_config(config, loop): 
    for i in range(len(config['seed_urls'])):
        if '://' not in config['seed_urls'][i]:
            config['seed_urls'][i] = 'http://' + config['seed_urls'][i]

    config['loop'] = loop
    
    return Crawler(config)
    
    
def start(config = '', logging_level = 2):
    """Main program.

    Parse arguments, set up event loop, run crawler, print report.
    """

    logging_levels = [logging.ERROR, logging.WARN, logging.INFO, logging.DEBUG]
    logging.basicConfig(level = logging_levels[min(logging_level, len(logging_levels)-1)])

    loop = asyncio.SelectorEventLoop()

    asyncio.set_event_loop(loop)
    crawler = get_crawler_from_config(config, loop)
    
    try:
        loop.run_until_complete(crawler.crawl())  # Crawler gonna crawl.
    except KeyboardInterrupt:
        sys.stderr.flush()
        print('\nInterrupted\n')
    finally:
        report(crawler)
        crawler.close()
        loop.close()



