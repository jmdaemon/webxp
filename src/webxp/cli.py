import re
import sys
import requests
import logging
from bs4 import BeautifulSoup

def main():
    '''
    Usage:
        webxp <subcmd> <url> options
    '''
    cmds = ['get']

    subcmd = None
    url = None
    opts = None
    for cmd in cmds:
        if cmd in sys.argv:
            subcmd = cmd.lower()
    if subcmd is None:
        print('Nothing to do')
        sys.exit(1)
    else:
        url = sys.argv[2]
        opts = sys.argv[3:]

    match subcmd:
        case "get": get(url, opts)
        case "post": post(url, opts)
        case "scrape": scrape(url, opts)

def get(url, opts):
    '''
    Sends a GET request to a specified url, and outputs the response

    Options:
        -r, --regex     : Filters by regex
        -t, --tags      : Filters by html tags
        -c, --css-class : Filters by css classes
        -s, --css       : Filters using css class selectors
        -r, --raw       : Outputs raw html content
    Examples:
        webxp get [url] -t p -s 'outer-text'
    '''

    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='lxml')

    # TODO: Create unified library for Get & Post requests
    # to specify request headers from command line arguments
    opt = opts[0]
    raw = opts[1]

    regex = ''
    css_classes = ''
    css_selectors = ''
    html_tags = ''
    raw = False

    # Set get arguments
    for i in range(len(opts)):
        # Parse filter options
        match opt:
            case '-t' | '--tags':
                html_tags = opts[i + 1]
            case '-c' | '--css-class':
                css_classes = opts[i + 1]
            case '-s' | '--css':
                css_selectors = opts[i + 1]
            case '-f' | '--filter':
                regex = opts[i + 1]
            case '-r' | '--raw':
                raw = True

    # Filter by html tags and/or css selectors
    html = ''
    if css_selectors:
        html = soup.select(css_selectors)
    else:
        html = soup.find_all(html_tags, class_=css_classes)

    # Additionally, filter the html by regex
    if (regex):
        # Compile regex
        pattern = re.compile(regex)
        results = pattern.findall(html.content)
        # Show all results
        for result in results:
            print(result)
        return

    if raw:
        # Prints the raw text
        print(html.extract().get_text())
    else:
        # Pretty print the html
        print(html.prettify())
    return

# TODO:
# Add ability to specify header fields
# Set default header file configurations
def post(url, opts):
    # Create headers & parse custom opts
    opt = opts[0]

    match opt:
        case "":
            pass

    # Create and send request
    r = requests.get(url)
    logging.info("Response:", r.content)

    # Yield html response
    soup = BeautifulSoup(r.content, features='lxml')

    # Show response to user
    print(soup.prettify())

# TODO:
# Combine with scrapy to follow links
# Add feature to grep content/text for specific keywords
def scrape(url, opts):
    ''' Scrapes the given site for information '''
    r = requests.get(url)
    logging.info("Response:", r.content)
    soup = BeautifulSoup(r.content, features='lxml')
    logging.info(soup.prettify())
