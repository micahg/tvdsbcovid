"""Docker script to automate answering the TVDSB covid screen utility."""
import os
import sys
import requests
from bs4 import BeautifulSoup

MAIN_PAGE = 'https://schoolapps2.tvdsb.ca/students/covid_screening_verification/index.aspx'
USER_INPUT = 'txtUsername'
PASS_INPUT = 'txtPassword'

FORM_ANSWER_NO = 'rdoOptions_1'
PAGE_SPAN_ERR_ID = 'lblError'


def process_form_soup(soup, user, pwd):
    """Process HTML for values."""
    form = soup.find('form')
    inputs = filter(lambda inp: not inp['id'] == FORM_ANSWER_NO, form.find_all('input'))
    form_vals = {inp['name']: inp['value'] if inp.has_attr('value') else None for inp in inputs}
    if USER_INPUT in form_vals:
        form_vals[USER_INPUT] = user
    if PASS_INPUT in form_vals:
        form_vals[PASS_INPUT] = pwd
    return form_vals


def request_page(sess, data=None):
    """Request the page."""
    resp = sess.get(MAIN_PAGE) if data is None else sess.post(MAIN_PAGE, data=data)
    if not resp.status_code == 200:
        print('HTTPS status {} when fetching {}'.format(resp.status, MAIN_PAGE))
        print('Response content: {}'.format(resp.content))
        sys.exit(1)

    soup = BeautifulSoup(resp.content, features="html.parser")
    error_span = soup.find('span', id=PAGE_SPAN_ERR_ID)
    error = "" if error_span is None else error_span.text
    if len(error) > 0:
        print('Page responds with error: "{}"'.format(error))
        sys.exit(1)

    return soup


def screen(user, pwd):
    """Screen a user."""
    print('Screening {}:{}'.format(user, pwd))

    sess = requests.Session()
    soup = request_page(sess)

    form_vals = process_form_soup(soup, user, pwd)
    soup = request_page(sess, form_vals)

    form_vals = process_form_soup(soup, user, pwd)
    soup = request_page(sess, form_vals)

    print('Result is "{}"'.format(soup.find('p').text))


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
