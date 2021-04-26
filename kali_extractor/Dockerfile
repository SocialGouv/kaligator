FROM python:3.7.10-stretch
WORKDIR /code
ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

RUN apt update
RUN apt install pv

ADD . /code
RUN pip install -e .
