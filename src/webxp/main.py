import os
import sys
import logging
from webxp.requests import get, post, scrape, scrapy, search

# loglevel = loglevel if loglevel else logging.ERROR
# if loglevel is None:
    # loglevel = logging.NOTSET

def main():
    '''
    Usage:
        webxp <subcmd> <url> options
    '''
    # Set the loglevel and default to no logging statements
    loglevel = os.environ.get("LOGLEVEL")
    # loglevel = loglevel if loglevel is not None else logging.NOTSET
    if loglevel is None:
        loglevel = logging.ERROR
    logging.basicConfig(level=loglevel)
    logging.info(f'Log level: {loglevel}')

    cmds = ['get', 'post', 'scrape', 'scrapy', 'search']

    subcmd = None
    url = None
    opts = None

    # Parse the subcommands
    for cmd in cmds:
        if cmd in sys.argv:
            subcmd = cmd.lower()
    if subcmd:
        logging.info('Subcommand: %s', subcmd)
    if subcmd is None:
        logging.info('Nothing to do')
        sys.exit(1)
    else:
        url = sys.argv[2]
        opts = sys.argv[3:]
    logging.info('Url: %s', url)
    logging.info('Options: %s', opts)

    match subcmd:
        case 'get': get(url, opts)
        case 'post': post(url, opts)
        case 'scrape': scrape(url, opts)
        case 'scrapy': scrape(url, opts)
        case 'search': search(url, opts)
