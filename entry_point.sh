#!/bin/sh
gunicorn --chdir /app barcode:app -w 2 --threads 2 -b 0.0.0.0:3333 --access-logfile '-'