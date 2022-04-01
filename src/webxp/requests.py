from bs4 import BeautifulSoup
from webxp.filters import filter_html
from webxp.cli import show_raw, show_response

import requests
import logging
import pandas as pd

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
    show_response(results)

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
    raw = show_raw(opts)
    results = filter_html(soup, opts, raw)
    show_response(results)

# TODO:
# Combine with scrapy to follow links
# Add feature to grep content/text for specific keywords
def scrape(url, opts):
    ''' Scrapes the given site for information '''
    logging.info('In scrape() function')
    r = requests.get(url)
    logging.info('Got Response')
    logging.debug('Response: %s', r.content)

    soup = BeautifulSoup(r.content, features='lxml')
    logging.info('Parsed html content')
    logging.debug('HTML Response: %s', soup.prettify())

    # Dispatch to various scraper backends
    for i in range(0, len(opts)):
        arg = opts[i]
        # Parse filter options
        match arg:
            case 'forecast.gov':
                logging.info('In forecast.gov')
                # seven_day = soup.find(id='seven-day-forecast')
                summary         = soup.find(id='current_conditions-summary')
                conditions      = soup.find(id='current_conditions_detail')
                current         = pd.read_html(r.content)
                temp_farenheit  = summary.find(class_='myforecast-current-lrg').get_text()
                temp_celsius    = summary.find(class_='myforecast-current-sm').get_text()

                logging.info(summary.prettify())
                logging.info(conditions.prettify())
                logging.info("Temperature Farenheit: %s", temp_farenheit)
                logging.info("Temperature Celsius: %s", temp_celsius)
                logging.info("Today's conditions:\n%s", current)

                df = current[0]
                print(df.head())
                # Display to user
                # print('Temperature: ', temp_celsius)

def scrapy(url, opts):
    pass
