FROM python:3.7.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /kmanga
WORKDIR /kmanga
COPY docker/requirements.txt /kmanga/
COPY docker/requirements/ /kmanga/requirements/
RUN apt-get -y update && apt-get -y upgrade && apt-get install libpq-dev
RUN pip install -r requirements.txt
COPY . /kmanga/
#CMD ["python", "--version"]
