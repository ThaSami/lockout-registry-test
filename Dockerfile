FROM python:3.8-alpine

ARG BUILD_DEPS="build-base gcc libffi-dev openssl-dev"
ARG RUNTIME_DEPS="libcrypto1.1 libssl1.1 libxml2-dev libxslt-dev curl jq ca-certificates openssl"
RUN apk add --no-cache git

RUN git config --global core.autocrlf false
COPY . /app
WORKDIR /app
RUN apk update \
 && apk add --no-cache --virtual .build-deps ${BUILD_DEPS} \
 && apk add --no-cache ${RUNTIME_DEPS} \
 && pip install --no-cache-dir -r requirements.txt \
 && apk del .build-deps \
 && find /usr/local \
        \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' \+


RUN chmod +x ./entry.sh
ENV METRICS_PORT 9200
ENV prometheus_multiproc_dir /tmp


ENTRYPOINT ["./entry.sh"]