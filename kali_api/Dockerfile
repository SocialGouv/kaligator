FROM python:3.7.10-stretch
WORKDIR /code

ADD requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

ADD . /code

CMD python app.py
