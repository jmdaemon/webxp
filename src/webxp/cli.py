import re
import sys
import requests
import logging
from bs4 import BeautifulSoup

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

def show_raw(opts):
    raw = False
    for i in range(len(opts)):
        arg = opts[i]
        match arg:
            case '-r' | '--raw':
                raw = True
                logging.info('Set raw : %s', raw)
    return raw

def filter_html(soup, opts, raw):
    '''
    Filter an html response

    Options:
        -r, --regex     : Filters by regex
        -t, --tags      : Filters by html tags
        -c, --css-class : Filters by css classes
        -s, --css       : Filters using css class selectors
        -r, --raw       : Outputs raw html content
    '''
    logging.info('In filter_html() function')
    regex = ''
    css_classes = ''
    css_selectors = ''
    html_tags = ''

    # Set get arguments
    for i in range(len(opts)):
        arg = opts[i]
        # Parse filter options
        match arg:
            case '-t' | '--tags':
                html_tags = opts[i + 1]
                logging.info('Set tags: %s', html_tags)
            case '-c' | '--css-class':
                css_classes = opts[i + 1]
                logging.info('Set css class: %s', css_classes)
            case '-s' | '--css':
                css_selectors = opts[i + 1]
                logging.info('Set css selector: %s', css_selectors)
            case '-f' | '--filter':
                regex = opts[i + 1]
                logging.info('Set regex: %s', regex)

    # Filter by html tags and/or css selectors
    html = BeautifulSoup()
    if css_selectors != '':
        html = soup.select(css_selectors)
        logging.info('Filter html with css selectors')
    else:
        html = soup.find_all(id=html_tags, class_=css_classes)
        logging.info('Filter html with html_tags & css classes')

    # Additionally, filter the html by regex
    if (regex):
        # Compile regex
        pattern = re.compile(regex)
        results = pattern.findall(html.content)
        logging.info('Filter html by regex')
        # Show all results
        # for result in results:
            # print(result)
        return results

    if raw:
        # Prints the raw text
        # print(html.extract().get_text())
        logging.info('Returning raw html')
        return html.extract().get_text()
    else:
        # Pretty print the html
        # print(html.prettify())
        logging.info('Returning prettified html')
        # print(html.prettify())
        print(html)
        # return html.prettify()
    return

def show_response(results, raw):
    ''' Display the filtered response '''
    # if (len(results) - 1 > 0):
    if (results is not None):
        if (len(results) > 0):
            if raw:
                for result in results:
                    print(result)
                    print()
            else:
                for result in results:
                    print(result.extract().get_text())
            return
        else:
            print(results)

def get(url, opts):
    '''
    Sends a GET request to a specified url, and outputs the response

    Examples:
        webxp get [url] -t p -s 'outer-text'
    '''

    logging.info('In get() function')
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='lxml')

    # TODO: Create unified library for Get & Post requests
    # to specify request headers from command line arguments
    # opt = opts[0]
    # raw = opts[1]
    raw = show_raw(opts)
    results = filter_html(soup, opts, raw)
    show_response(results, raw)

# TODO:
# Add ability to specify header fields
# Set default header file configurations
def post(url, opts):
    logging.info('In post() function')
    # Create headers & parse custom opts
    # opt = opts[0]

    # match opt:
        # case '':
            # pass

    # Create and send request
    r = requests.get(url)
    logging.debug('Response: %s', r.content)

    # Yield html response
    soup = BeautifulSoup(r.content, features='lxml')

    # Show response to user
    results = filter_html(opts)
    show_response(results)

# TODO:
# Combine with scrapy to follow links
# Add feature to grep content/text for specific keywords
def scrape(url, opts):
    ''' Scrapes the given site for information '''
    logging.info('In scrape() function')
    r = requests.get(url)
    logging.debug('Response: %s', r.content)
    soup = BeautifulSoup(r.content, features='lxml')
    logging.debug('HTML Response: %s', soup.prettify())

    # Dispatch to various scraper backends
    for i in range(len(opts)):
        arg = opts[i]
        # Parse filter options
        match arg:
            case 'forecast.gov':
                # seven_day = soup.find(id='seven-day-forecast')
                summary = soup.find(id='current_conditions-summary')
                conditions = soup.find(id='current_conditions_detail')
                temp_farenheit = summary.find(class_='myforecast-current-lrg').get_text()
                temp_celsius = summary.find(class_='myforecast-current-sm').get_text()

                # Display to user
                logging.info(summary.prettify())
                logging.info(conditions.prettify())

                print('Temperature: ', temp_celsius)
def scrapy(url, opts):
    pass
