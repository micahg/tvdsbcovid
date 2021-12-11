"""Docker script to automate answering the TVDSB covid screen utility."""
import os
import sys

MAIN_PAGE = 'https://schoolapps2.tvdsb.ca/students/covid_screening_verification/index.aspx'


def screen(user, pwd):
    print('Screening {}:{}'.format(user,pwd))


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

for user, pwd in dict(zip(users, passes)).items():
    screen(user, pwd)
