#!/bin/sh

WORKERS=${WORKERS:-2}
PORT=${API_PORT:-5000}

cd api && gunicorn -c config.py app:app -w ${WORKERS} -b 0.0.0.0:${PORT}