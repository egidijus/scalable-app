FROM library/python:alpine3.7
RUN apk add --update \
    python3 \
  && rm -rf /var/cache/apk/* \
  && ln -s /usr/bin/pip3 /usr/bin/pip \
  && ln -s /usr/bin/python3 /usr/bin/python

ADD . /opt/src
WORKDIR /opt/src

RUN pip install -r /opt/src/requirements.txt

EXPOSE 8448
CMD ["python", "src/app.py"]
