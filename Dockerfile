# Base Image
FROM python:3

# create and set working directory
RUN mkdir /code
WORKDIR /code

# Add current directory code to working directory
ADD . /code/

# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install project dependencies
RUN pip install django
RUN pip install -r requirements.txt

COPY . /code/