# Pull the base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code

RUN apt-get update
RUN pip install pip -U

#Upgrade pip
ADD requirements.txt /code/
#Install dependencies
RUN pip install -r requirements.txt
ADD . /code/