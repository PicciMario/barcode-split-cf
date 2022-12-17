FROM python:3.10-slim
RUN mkdir -p /app
WORKDIR /app
RUN apt-get update && apt-get -y install zbar-tools poppler-utils
RUN apt-get clean
ADD app/requirements.txt /app/
RUN pip install -r requirements.txt
ADD app/barcode.py app/entry_point.sh /app/
EXPOSE 3333
ENTRYPOINT ["./entry_point.sh"]