# from . import login


# __all__ = ["login"]


def login(browser, subdomain, email, password):
    print('Logging in to {} as {}.'.format(subdomain, email))

    login_url = 'https://{}/?no_sso=1'.format(subdomain)

    browser.visit(login_url)

    browser.find_by_xpath('//*[@id="email"]').fill(email)
    browser.find_by_xpath('//*[@id="password"]').fill(password)
    submit = browser.find_by_xpath('//*[@id="signin_btn"]')
    submit.click()


def load_current_emojis(browser, subdomain):

    emoji_url = 'https://{}/customize/emoji'.format(subdomain)

    browser.visit(emoji_url)

    emojis = []
    emojis_text = browser.find_by_xpath('//*[@headers="custom_emoji_name"]')
    emojis_type = browser.find_by_xpath('//*[@headers="custom_emoji_type"]')

    for item in range(0, len(emojis_text)):
        emojis.append(
            (emojis_text[item].text, emojis_type[item].text)
        )

    # import ipdb ; ipdb.set_trace()
