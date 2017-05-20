import os
import yaml
import requests
import sys
from time import sleep
import urllib
# from . import login


# __all__ = ["login"]

ACCEPTED_IMAGES = ['gif', 'jpg', 'png']


class Emoji(object):
    EMOJI_TYPES = [
        'IMAGE',
        'ALIAS',
    ]

    def __init__(self, emoji_name, emoji_type):
        self.name = self._clean_name(emoji_name)
        self.type, self.alias = self._determine_type(emoji_type)

    def _clean_name(self, name):
        return name[1:-1]

    def _determine_type(self, emoji_type):
        if 'Alias for :' == emoji_type[:11]:
            return 'ALIAS', emoji_type[11:-1]
        return 'IMAGE', None


def login(browser, subdomain, email, password):
    print('Logging in to {} as {}.'.format(subdomain, email))

    login_url = 'https://{}/?no_sso=1'.format(subdomain)

    browser.visit(login_url)

    browser.find_by_xpath('//*[@id="email"]').fill(email)
    browser.find_by_xpath('//*[@id="password"]').fill(password)
    submit = browser.find_by_xpath('//*[@id="signin_btn"]')
    submit.click()


def load_current_emojis(browser, subdomain):
    print('Loading the currently installed emojis.')

    emoji_url = 'https://{}/customize/emoji'.format(subdomain)

    browser.visit(emoji_url)

    emojis = {}
    emojis_name = browser.find_by_xpath('//*[@headers="custom_emoji_name"]')
    emojis_type = browser.find_by_xpath('//*[@headers="custom_emoji_type"]')

    for item in range(0, len(emojis_name)):
        emoji = Emoji(
            emojis_name[item].text,
            emojis_type[item].text,
        )

        emojis[emoji.name] = emoji

    return emojis


def load_emojipack_yml(pack, cache_directory='./.cache'):
    print('Load the YAML file')

    if pack[:4] == 'http':
        # Load remote
        response = requests.get(pack)
        if response.status_code == 200:
            yaml_text = response.text
        else:
            sys.exit(-1)
    else:
        if not os.path.exists(pack):
            sys.exit(-1)
        file = open(pack, 'r')
        yaml_text = file.read().strip()
        file.close()

    yaml_contents = yaml.load(yaml_text)

    emojis = []

    if not os.path.exists(cache_directory):
        os.mkdir(cache_directory)

    for emoji in yaml_contents['emojis']:

        # Check the extension
        extension = emoji['src'][-3:].lower()

        if extension not in ACCEPTED_IMAGES:
            print('{} does not have an accepted extension ({}).  Ignoring.'.format(
                emoji['name'],
                extension,
            ))
            continue

        emoji['image'] = '{}/{}.{}'.format(
            cache_directory,
            emoji['name'],
            extension,
        )

        urllib.request.urlretrieve(emoji['src'], emoji['image'])

        emojis.append(emoji)

    return emojis


def install_emojipack(browser, subdomain, emojis, emoji_yaml):
    print('Now installing emojis...')

    for emoji in emoji_yaml:
        if emoji['name'] in emojis:
            print('    {} already uploaded.  Skipping.'.format(emoji['name']))
        else:
            _upload_emoji(browser, subdomain, emoji['name'], emoji['image'])
            print('    {} installed.'.format(emoji['name']))

        for alias in emoji.get('aliases', []):
            if alias in emojis:
                print('        Alias {} already set.  Skipping.'.format(emoji['name']))
            else:
                _alias_emoji(browser, subdomain, alias, emoji['name'])
                print('        Alias {} set.'.format(alias))


def _upload_emoji(browser, subdomain, name, filename):
    emoji_url = 'https://{}/customize/emoji'.format(subdomain)
    browser.visit(emoji_url)
    sleep(2)
    browser.find_by_xpath('//*[@id="emojiname"]').fill(name)
    browser.attach_file('img', os.path.abspath(filename))

    submit_button = browser.find_by_xpath('//*[@id="addemoji"]/div[2]/p[4]/input')

    submit_button.click()

    return True


def _alias_emoji(browser, subdomain, name, emoji_name):
    emoji_url = 'https://{}/customize/emoji'.format(subdomain)
    browser.visit(emoji_url)
    sleep(2)
    browser.find_by_xpath('//*[@id="emojiname"]').fill(name)
    browser.find_by_xpath('//*[@id="set_emoji_alias"]/a').click()

    sleep(1)
    emoji_search_box = browser.find_by_xpath('//*[@id="emoji_input"]')

    emoji_search_box.fill(emoji_name)
    browser.find_by_xpath('//*[@id="emoji_menu_items_div"]/div[1]/div/div/div/a').click()

    submit_button = browser.find_by_xpath('//*[@id="addemoji"]/div[2]/p[4]/input')

    submit_button.click()

    return True
