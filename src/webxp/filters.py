from bs4 import BeautifulSoup

import re
import logging

def get_filters(opts):
    ''' Extracts the cli args to filter the html requests '''
    regex = ''
    css_classes = ''
    css_selectors = ''
    html_tags = ''

    # Set get arguments
    for i in range(0, len(opts)):
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
            case '-r' | '--regex':
                regex = opts[i + 1]
                logging.info('Set regex: %s', regex)

    return (regex, css_classes, css_selectors, html_tags)

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
    (regex, css_classes, css_selectors, html_tags) = get_filters(opts)

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
        # If logging is set to debug
        if logging.root.level >= logging.DEBUG:
            # Show all results
            for result in results:
                print(result)
        return results

    if raw:
        # Prints the raw text
        logging.info('Returning prettified html')
        results = []
        for result in html:
            results.append(result.extract().get_text())
    else:
        logging.info('Returning raw html')
        return html
