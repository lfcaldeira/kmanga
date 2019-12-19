FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /kmanga
WORKDIR /kmanga
COPY requirements.txt /kmanga/
COPY requirements/ /kmanga/requirements/
RUN pip install -r requirements.txt
COPY . /kmanga/
