# Endpoint HTTP per splittare un documento a partire dai barcode sulle pagine. Esperimento di applicazione Docker su SAP Cloud Foundry.

Crea un endpoint POST che riceve un PDF come payload. Individua la presenza di barcode che seguono un determinato pattern, e li utilizza come indicatori di inizio delle parti in cui è diviso il documento. Divide il documento in singoli PDF e li restituisce al chiamante sotto forma di multipart.

# Istruzioni per il deployment

## Prerequisiti
- Account BTP Cloud Foundry (anche [account trial](https://account.hanatrial.ondemand.com/trial/#/home/trial)).
- Installazione sulla propria macchina di [tools cli](https://github.com/cloudfoundry/cli/releases) per Cloud Foundry.
- Installazione Docker sulla propria macchina.
- Account su [Docker Hub](https://hub.docker.com/).

## Step preliminari

- Configurare tools cf con endpoint corretto per la propria istanza BTP:

	`cf api https://api.cf.eu20.hana.ondemand.com`

- Effettuare login sulla CF con il proprio utente:

	`cf login`

## Creazione servizio XSUAA

Prima di procedere configurare a dovere il file `xsuaa/xs-security.json`

`cf create-service xsuaa application barcode-split-xsuaa -c xsuaa/xs-security.json`

## Creare immagine Docker

Creare immagine docker (nota: come prefisso del tag usare il proprio nome account su Docker Hub).

`docker build -t piccimario/barcode-split-cf:0.1 .`

(facoltativo) Test in locale (viene esposta la porta 3333). L'opzione `--rm` serve a eliminare l'istanza (container) di test quando viene fermata. Le opzioni `-t` e `-i` sono utili durante i test perchè forzano l'allocazione di un terminale e lasciano il container in modalità interattiva, il che ci permette di terminarlo usando Ctrl+C.

`docker run -t -i --rm -p 3333:3333 piccimario/barcode-split-cf:0.1`

## Caricamento immagine su Docker Hub
`docker push piccimario/barcode-split-cf:0.1`

> Nota: ogni volta che si esegue il push dell'immagine sulla CF, questa ha bisogno della password dell'account Docker per il recupero. Per evitare diinserire ogni volta la password, questa può essere impostata come variabile d'ambiente (sarà usabile fino alla chiusura del terminale).
>
> Terminale BASH: export CF_DOCKER_PASSWORD="xxxxxxxxxx"

## Caricamento applicazione e approuter su Cloud Foundry:

`cf push`

> Nota: nel file manifest.yaml si configurano i dettagli relativi all'immagine docker da utilizzare (in particolare il nome e il prefisso, che deve corrispondere al proprio utente Docker Hub).

---

## Risorse varie:

- https://adamtheautomator.com/flask-web-server/

- https://blogs.sap.com/2021/01/02/deploy-python-application-on-sap-cloud-platform-using-docker-container/

- https://techtutorialsx.com/2020/01/01/python-pyzbar-detecting-and-decoding-barcode/

- https://barcode.tec-it.com (servizio gratuito per generare immagini di barcode in diversi formati)