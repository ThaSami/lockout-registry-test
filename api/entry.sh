#!/bin/sh

BRANCH_NAME=${BRANCH_NAME:-main}
WORKERS=${WORKERS:-2}
PORT=${API_PORT:-5000}
git reset --hard HEAD
git pull --all
git checkout ${BRANCH_NAME}
git pull --all

gunicorn -c config.py app:app -w ${WORKERS} -b 0.0.0.0:${PORT}