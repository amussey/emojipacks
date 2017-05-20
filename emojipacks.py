#!/usr/bin/env python3

import click
import os
from splinter import Browser

import emojipacks


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
def runner(debug, subdomain, email, password, emoji_dir, pack, save):
    if emoji_dir is None and pack is None:
        pack = click.prompt(PACK_PROMPT)

    emoji_yaml = emojipacks.load_emojipack_yml(pack)

    browser = Browser('chrome')
    emojipacks.login(browser, subdomain, email, password)

    emojis = emojipacks.load_current_emojis(browser, subdomain)

    # import ipdb ; ipdb.set_trace()

    emojipacks.install_emojipack(browser, subdomain, emojis, emoji_yaml)

    browser.quit()

    click.secho('All emojis installed!', fg='green', bold=True)


if __name__ == '__main__':
    runner()
