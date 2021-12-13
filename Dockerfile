FROM python:3.9-alpine

RUN python -m pip install requests beautifulsoup4

COPY screening.py ./

CMD [ "python", "./screening.py" ]
