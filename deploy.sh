cf create-service xsuaa application barcode-split-xsuaa -c xsuaa/xs-security.json
docker build -t piccimario/barcode-split-cf:0.1 .
docker push piccimario/barcode-split-cf:0.1
cf push