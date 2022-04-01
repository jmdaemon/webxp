import sys
import logging
from webxp.requests import get, post, scrape, scrapy

# Set logging level
logging.basicConfig(level=logging.INFO)

def main():
    '''
    Usage:
        webxp <subcmd> <url> options
    '''
    cmds = ['get', 'post', 'scrape', 'scrapy']

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
        print('Nothing to do')
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
