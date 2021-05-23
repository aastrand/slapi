FROM tiangolo/meinheld-gunicorn-flask:python3.8

COPY requirements.txt /
RUN pip3 install -r /requirements.txt

RUN mkdir app
RUN mkdir app/static
COPY slapi/*.py /app
COPY slapi/static/* /app/static
