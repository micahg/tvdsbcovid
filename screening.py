"""Docker script to automate answering the TVDSB covid screen utility."""
import os
import sys
import requests
from bs4 import BeautifulSoup

MAIN_PAGE = 'https://schoolapps2.tvdsb.ca/students/covid_screening_verification/index.aspx'
USER_INPUT = 'txtUsername'
PASS_INPUT = 'txtPassword'


def process_form_soup(soup, user, pwd):
    """Process HTML for values."""
    form = soup.find('form')
    inputs = filter(lambda inp: not inp['id'] == 'rdoOptions_1', form.find_all('input'))
    form_vals = {inp['name']: inp['value'] if inp.has_attr('value') else None for inp in inputs}
    if USER_INPUT in form_vals:
        form_vals[USER_INPUT] = user
    if PASS_INPUT in form_vals:
        form_vals[PASS_INPUT] = pwd
    return form_vals


def screen(user, pwd):
    """Screen a user."""
    print('Screening {}:{}'.format(user, pwd))

    sess = requests.Session()
    resp = sess.get(MAIN_PAGE)
    if not resp.status_code == 200:
        print('HTTPS status {} when fetching {}'.format(resp.status, MAIN_PAGE))
        print('Response content: {}'.format(resp.content))
        sys.exit(1)

    soup = BeautifulSoup(resp.content, features="html.parser")

    form_vals = process_form_soup(soup, user, pwd)

    resp = sess.post(MAIN_PAGE, data=form_vals)
    if not resp.status_code == 200:
        print('HTTPS status {} when fetching {}'.format(resp.status, MAIN_PAGE))
        print('Response content: {}'.format(resp.content))
        sys.exit(1)

    soup = BeautifulSoup(resp.content, features="html.parser")
    error_span = soup.find('span', id='lblError')
    error = "" if error_span is None else error_span.text
    if len(error) > 0:
        print('Page responds with error: "{}"'.format(error))
        sys.exit(1)

    form_vals = process_form_soup(soup, user, pwd)

    resp = sess.post(MAIN_PAGE, data=form_vals)
    if not resp.status_code == 200:
        print('HTTPS status {} when fetching {}'.format(resp.status, MAIN_PAGE))
        print('Response content: {}'.format(resp.content))
        sys.exit(1)

    soup = BeautifulSoup(resp.content, features="html.parser")
    print(soup.find('p').text)


if 'USER' not in os.environ:
    print('Unable to get user list from environment. Please consult documentation.')
    sys.exit(1)

if 'PASS' not in os.environ:
    print('Unable to get pass list from environment. Please consult documentation.')
    sys.exit(1)

users = os.environ['USER'].split(',')
passes = os.environ['PASS'].split(',')

if len(users) != len(passes):
    print('Length for users and passes different. Please consult documentation.')
    sys.exit(1)

for k, v in dict(zip(users, passes)).items():
    screen(k, v)
