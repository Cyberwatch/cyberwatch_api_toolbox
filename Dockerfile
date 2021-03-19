FROM python:3.9-slim

ENV INSTALL_PATH=/api

WORKDIR $INSTALL_PATH

COPY . .

RUN python setup.py install

ENTRYPOINT ["/usr/local/bin/cyberwatch-cli"]
