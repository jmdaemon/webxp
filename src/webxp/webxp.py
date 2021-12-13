#!/bin/python

# import click
import sys
import requests
from bs4 import BeautifulSoup


def main():
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



# @cli.command()
# @click.option('-t', 'tags', required=False, multiple=True)
# @click.option('-s', 'strip', required=False, is_flag=True)
# @click.option('-R', 'regex', required=False)
# @click.argument('url', metavar='<url>', required=True)
# @click.pass_obj
# def get(page, url, tags, strip, regex):
def get(url, opts):
    # get receives a url and a list of attributes,these attributes
    # are iterated to get the current line which has the html tags extracted and pushed
    # Send request
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='lxml')

    # Input is passed like so:
    # webxp <subcmd> <url> options
    # options for get are
    # -f, --filter: filters by regex
    # -t, --tags : Filters by specific html tags only
    # Combinable
    # -r, --raw : Outputs raw contents of either tags or entire tree

    # output = []
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
    # for out in output:
        # print(output)

    # if not tags:
        # print(soup.prettify())
        # return

    # # for tag in tags:
    # # print(type(tags))
    # if not strip: # Strip tags
        # # for att in soup.find_all(tags):
        # for tag in soup.find_all(list(tags)):
            # print(tag.prettify())
    # else: # Output raw
        # for tag in soup.find_all(tags):
            # print(tag.extract().get_text())

if __name__ == '__main__':
    main()
    # cli()

