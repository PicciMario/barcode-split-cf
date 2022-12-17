import sys
import requests
import json

# Informazioni importate da file esterno per non metterle su github
# username e password sono relative all'utente (non necessarie per client_credentials)
# gli altri parametri si possono vedere nella btp nel servizio xsuaa, "view credentials"
from credentials import username, password, auth_server_url, client_id, client_secret

# Nota: questo meccanismo bypassa l'approuter e chiama direttamente il servizio dopo
# aver recuperato il token. Attenzione se l'approuter è usato, per esempio, per manipolare
# l'indirizzo chiamato mediante route.

# Disabilita warning per mancata verifica del certificato del server
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

###############################################################################

def get_new_token():

	type = 0

	if type == 0:

		print("Richiesta token con grant: CLIENT_CREDENTIALS")

		token_req_payload = {
			'grant_type': 'client_credentials'
		}

		token_response = requests.post(
			auth_server_url + '/oauth/token',
			data=token_req_payload, 
			verify=False, 
			allow_redirects=False,
			auth=(client_id, client_secret)
		)

	elif type == 1:

		print("Richiesta token con grant: PASSWORD")

		token_req_payload = {
			'grant_type': 'password',
			'username': username,
			'password': password,
		}

		token_response = requests.post(
			auth_server_url + '/oauth/token',
			data=token_req_payload, 
			verify=False, 
			allow_redirects=False,
			auth=(client_id, client_secret)
		)
				
	if token_response.status_code !=200:
		print("Failed to obtain token from the OAuth 2.0 server", file=sys.stderr)
		sys.exit(1)

	print("Successfuly obtained a new token")
	tokens = json.loads(token_response.text)
	return tokens['access_token']

###############################################################################

token = get_new_token()

test_api_url = "https://barcode-split.cfapps.us10-001.hana.ondemand.com/"
api_call_headers = {'Authorization': 'Bearer ' + token}
api_call_response = requests.get(test_api_url, headers=api_call_headers)

print(api_call_response.text)
