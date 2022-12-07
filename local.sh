docker build -t piccimario/barcode-split-cf:0.1 .
docker run -t -i --rm -p 3333:3333 piccimario/barcode-split-cf:0.1