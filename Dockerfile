FROM python:3.9-alpine

RUN pip install requests

COPY screening.py ./

CMD [ "python", "./screening.py" ]
