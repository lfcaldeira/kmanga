FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update && apt-get -y upgrade && apt-get install libpq-dev
COPY ./entrypoint.sh /
RUN chmod a+x entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
#CMD ["tail","-f","/dev/null"]
CMD ["python", "/kmanga/kmanga/manage.py", "runserver", "0.0.0.0:8000"]
#RUN pip install -r requirements.txt
#COPY . /kmanga/
#CMD ["python", "--version"]
