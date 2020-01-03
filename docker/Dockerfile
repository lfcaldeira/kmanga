FROM python:3.6
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y --no-install-recommends \
		libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /requirements
COPY ./requirements/* ./

RUN pip install -r production.txt

RUN mkdir /kindlegen
RUN wget -qO- http://kindlegen.s3.amazonaws.com/kindlegen_linux_2.6_i386_v2_9.tar.gz | tar xzvf - -C /kindlegen

WORKDIR /

COPY ./entrypoint.sh /
RUN chmod a+x entrypoint.sh
#ENTRYPOINT ["/entrypoint.sh"]



#CMD ["python", "/site/kmanga/manage.py", "runserver", "0.0.0.0:8000"]
