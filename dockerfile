FROM python:3.7-slim-buster

USER root

WORKDIR /home

RUN apt-get update

RUN apt-get -y install gcc curl nano python3-dev python3-pip libxml2-dev libxslt1-dev zlib1g-dev g++

RUN python -m pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY assets /home/assets
COPY data /home/data
COPY app.py /home
COPY _users.py /home

EXPOSE 5050

HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://172.31.40.44:5050/health_check || exit 1

CMD python app.py
