#!/bin/sh
gunicorn --chdir /app barcode:app -w 1 --threads 1 -b 0.0.0.0:3333 --access-logfile '-'