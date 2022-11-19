FROM python:3.10-slim
RUN mkdir -p /app
WORKDIR /app
RUN apt-get update && apt-get -y install zbar-tools poppler-utils
RUN apt-get clean
RUN pip install flask pyzbar pdf2image cfenv gunicorn PyPDF2 requests_toolbelt
ADD barcode.py entry_point.sh /app/
EXPOSE 3333
ENTRYPOINT ["./entry_point.sh"]