#!/bin/python3.9

import click
import requests
from bs4 import BeautifulSoup


class Page(object):
    # def __init__(self, url=None, verbose=False):
        # self.url = url
    def __init__(self, verbose=False):
        self.verbose = verbose

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

@click.group(options_metavar='[options]', context_settings=CONTEXT_SETTINGS)
@click.option('-V'   , '--version'      , 'version'     , help='Show program version'           , is_flag=True, default=False)
@click.option('-v'   , '--verbose'      , 'verbose'     , help='Display verbose output'         , is_flag=True, default=False)
# @click.option('-v'   , '--verbose'      , 'verbose'     , help='Display verbose output'         , is_flag=True, default=False)
# @click.argument('url', metavar='<url>', required=True)
@click.pass_context
# def cli(ctx, url, version, verbose):
def cli(ctx, version, verbose):
    ctx.obj = Page(verbose)


@cli.command()
@click.option('-t', 'tags', required=False, multiple=True)
@click.option('-s', 'strip', required=False, is_flag=True)
@click.option('-R', 'regex', required=False)
@click.argument('url', metavar='<url>', required=True)
@click.pass_obj
def get(page, url, tags, strip, regex):
    # get receives a url and a list of attributes,these attributes
    # are iterated to get the current line which has the html tags extracted and pushed
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features='lxml')

    output = []
    if not tags:
        print(soup.prettify())
        return

    # for tag in tags:
    # print(type(tags))
    if not strip:
        # for att in soup.find_all(tags):
        for tag in soup.find_all(list(tags)):
            print(tag.prettify())
    else:
        for tag in soup.find_all(tags):
            print(tag.extract().get_text())

if __name__ == '__main__':
    cli()

