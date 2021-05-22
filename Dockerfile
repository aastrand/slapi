FROM python:3.8.10-alpine3.13

COPY requirements.txt /
RUN pip3 install -r requirements.txt

RUN mkdir slapi
RUN mkdir slapi/static
COPY slapi/*.py slapi
COPY slapi/static/* slapi/static

ENV PYTHONPATH .
ENTRYPOINT python3 slapi/app.py