FROM ubuntu
# FROM python
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install wget python3-pip python3-dev -y

RUN pip3 install requests
RUN pip3 install pymongo

ADD . /app
WORKDIR /app