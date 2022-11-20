# Endpoint HTTP per splittare un documento a partire dai barcode sulle pagine. Esperimento di applicazione Docker su SAP Cloud Foundry.

Crea un endpoint POST che riceve un PDF come payload. Individua la presenza di barcode che seguono un determinato pattern, e li utilizza come indicatori di inizio delle parti in cui è diviso il documento. Divide il documento in singoli PDF e li restituisce al chiamante sotto forma di multipart.

## Creazione immagine Docker

- Richiede Docker sulla macchina locale.

- Creare account su [Docker Hub](https://hub.docker.com/).

- Creare immagine docker (nota: come prefisso del tag usare il proprio nome account su Docker Hub).

	`docker build -t piccimario/barcode-split-cf:0.1 .`

- Test in locale (viene esposta la porta 3333). L'opzione `--rm` serve a eliminare l'istanza (container) di test quando viene fermata. Le opzioni `-t` e `-i` sono utili durante i test perchè forzano l'allocazione di un terminale e lasciano il container in modalità interattiva, il che ci permette di terminarlo usando Ctrl+C.

	`docker run -t -i --rm -p 3333:3333 piccimario/barcode-split-cf:0.1`

- Push su Docker Hub.

	`docker push piccimario/barcode-split-cf:0.1`

## Caricamento immagine su Cloud Foundry:

- Creare [account trial](https://account.hanatrial.ondemand.com/trial/#/home/trial).
- Installare [tools cli](https://github.com/cloudfoundry/cli/releases) per Cloud Foundry.
- `cf api https://api.cf.eu20.hana.ondemand.com` (usare endpoint cf corretto per il proprio trial)
- `cf login`
- `cf push barcode-split --docker-image piccimario/barcode-split-cf:0.1 --docker-username piccimario -k 512M -m 512M`

---

## Risorse varie:

- https://adamtheautomator.com/flask-web-server/

- https://blogs.sap.com/2021/01/02/deploy-python-application-on-sap-cloud-platform-using-docker-container/

- https://techtutorialsx.com/2020/01/01/python-pyzbar-detecting-and-decoding-barcode/

- https://barcode.tec-it.com (servizio gratuito per generare immagini di barcode in diversi formati)