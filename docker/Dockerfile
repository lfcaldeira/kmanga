FROM python:3.7.5
ENV PYTHONUNBUFFERED 1
#WORKDIR /kmanga
#COPY ./docker/requirements.txt /kmanga/
#COPY ./docker/requirements/ /kmanga/requirements/
RUN apt-get -y update && apt-get -y upgrade && apt-get install libpq-dev
COPY ./entrypoint.sh /
RUN chmod a+x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["ls"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#RUN pip install -r requirements.txt
#COPY . /kmanga/
#CMD ["python", "--version"]
