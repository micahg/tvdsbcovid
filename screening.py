"""Docker script to automate answering the TVDSB covid screen utility."""
import os

MAIN_PAGE = 'https://schoolapps2.tvdsb.ca/students/covid_screening_verification/index.aspx'

print('running...')
for k, v in os.environ.items():
    print('\t{}={}'.format(k, v))
