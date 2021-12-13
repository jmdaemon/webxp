import sys
import requests
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

def get(url, opts):
    '''
    Sends a GET request to a specified url, and outputs the response
    Options:
        -f, --filter: filters by regex
        -t, --tags : Filters by specific html tags only
    Combinable
        -r, --raw : Outputs raw contents of either tags or entire tree
    '''

    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='lxml')

    assert(len(opts) <= 1) # Ignore combinable ops for now
    opt = opts[0]
    match opt:
        case '-f' | '--filter':
            tags = opts[1:]
            for tag in tags:
                # output.append(type(tag))
                print(type(tag))
            # return
        case '-t' | '--tags':
            tags = opts[1:]
            for tag in soup.find_all(tags):
                print(tag.extract().get_text())
        case _:
            # output.append(soup.prettify())
            print(soup.prettify())
            # return
    return
