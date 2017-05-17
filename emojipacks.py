#!/usr/bin/env python3

import click


@click.command()
@click.option('-d', '--debug', help='Run in debug mode', default=False, type=(bool))
@click.option('-s', '--subdomain', prompt='Slack subdomain', help='Your Slack subdomain', type=(str))
@click.option('-e', '--email', prompt='Email address login', help='Admin email address.', type=(str))
@click.option('-p', '--password', prompt='Password', help='Password for admin email', type=(str))
@click.option('-y', '--pack', prompt='Path or URL of Emoji yaml file', help='YAML emoji pack', type=(str))
def emojipacks(debug, subdomain, email, password, pack):
    print(debug, subdomain, email, password, pack)


if __name__ == '__main__':
    emojipacks()
