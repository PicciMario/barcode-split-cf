import requests, os, re
from requests_toolbelt.multipart import decoder

# File di test da inviare
with open('./test_bc_multipli_doc.pdf', 'rb') as f:
	data = f.read()

# Riceve risposta dal servizio
res = requests.post(
	url='http://localhost:3333/barcodesplit',
	data=data,
	headers={'Content-Type': 'application/octet-stream'}
)

# Estrae multipart risposta
multipart_data = decoder.MultipartDecoder.from_response(res)

# Analizza singole parti del multipart
r = re.compile('^filename="([A-Za-z0-9-\.]+)"$')
for part in multipart_data.parts:

	headers = {k.decode(): v.decode() for k,v in dict(part.headers).items()}
	content_disp = [x.strip() for x in headers['Content-Disposition'].split(';')]
	filename = [r.search(x).group(1) for x in content_disp if r.match(x)][0]

	with open(os.path.join('./', filename), 'wb') as file:
		file.write(part.content)