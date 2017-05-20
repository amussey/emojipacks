#!/usr/bin/env python3

import click
import os
from splinter import Browser
# import ipdb
# from time import sleep

import emojipacks2


ACCEPTED_IMAGES = ['gif', 'jpg', 'png']
PACK_PROMPT = 'Path or URL of Emoji YAML file'

URLS = {
    'loginFormPath': '/?no_sso=1',
    'emojiUploadFormPath': '/admin/emoji',
    'emojiUploadImagePath': '/customize/emoji',
}


@click.command()
@click.option('-d', '--debug', help='Run in debug mode', default=False, type=(bool))
@click.option('-s', '--subdomain', default='lgtm.slack.com', prompt='Slack subdomain', help='Your Slack subdomain', type=(str))
@click.option('-e', '--email', default=os.environ.get('EMOJI_EMAIL'), prompt='Email address login', help='Admin email address.', type=(str))
@click.option('-p', '--password', default=os.environ.get('EMOJI_PASS'), prompt='Password', help='Password for admin email', type=(str))
@click.option('-x', '--emoji-dir', help='A directory with emoji images.', type=(str))
@click.option('-y', '--pack', help='YAML emoji pack', type=(str))
@click.option('-s', '--save', help='Save the credentials to a temp file.', default=True, type=(bool))
def emojipacks(debug, subdomain, email, password, emoji_dir, pack, save):
    if emoji_dir is None and pack is None:
        pack = click.prompt(PACK_PROMPT)
    # print(debug, subdomain, email, password, pack)

    browser = Browser('chrome')
    emojipacks2.login(browser, subdomain, email, password)

    emojipacks2.load_current_emojis(browser, subdomain)

    browser.quit()


if __name__ == '__main__':
    emojipacks()
