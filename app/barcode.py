import os, json, re, io, logging, uuid, time
from flask import Flask, request, Response, send_from_directory
from pyzbar import pyzbar
import pdf2image
from PyPDF2 import PdfFileWriter, PdfFileReader
from cfenv import AppEnv
from requests_toolbelt import MultipartEncoder
from sap.cf_logging import flask_logging
from sap import xssec

env = AppEnv()
uaa_service = env.get_service(name='barcode-split-xsuaa').credentials

app = Flask(__name__)

# Global variables
SECURITY_CONTEXT = "security_context"
globals = {}

# Initialize logging
flask_logging.init(app, logging.INFO)

# Temp folder path
TMP_DIR = r'/tmp/'

###############################################################################

@app.before_request
def check_credentials():

	global globals

	auth_header = request.headers.get('Authorization')

	if not auth_header:
		return "Errore: nessun header autorizzativo!", 403

	try:
		auth_token = auth_header.split(" ")[1]
		globals[SECURITY_CONTEXT] = xssec.create_security_context(auth_token, uaa_service)
	except:
		return "Errore: token errato!", 403

###############################################################################

@app.route('/', methods=['GET'])
def info():

	global globals 

	isAuthorized = globals[SECURITY_CONTEXT].check_scope(f"{uaa_service['xsappname']}.split")
	grant_type = globals[SECURITY_CONTEXT].get_grant_type()
	logon_name = globals[SECURITY_CONTEXT].get_logon_name()

	text = (
		f"<h1>Barcode services up&running!</h1>"
		f"<ul>"
		f"<li>Split scope available: {isAuthorized}</li>"
		f"<li>Grant type: {grant_type}</li>"
		f"<li>Logon name: {logon_name}</li>"
		f"</ul>"
	)

	return(text)

###############################################################################

def calc_split_positions(pages, pattern=None, barcode_type='CODE128'):

	"""
	Calculates split positions by looking for barcodes which follow the specified pattern (if provided).
	Returns a list of tuples (page number, barcode value).
	"""
	
	split_positions = []

	for index, page in enumerate(pages):
		found_barcodes = pyzbar.decode(page)
		for obj in found_barcodes:
			
			# print(f"Barcode {obj.data.decode('utf-8')} (type {obj.type}) found on page {index}")
			
			if (obj.type != barcode_type): continue
			if (pattern and not pattern.match(obj.data.decode('utf-8'))): continue
			
			split_positions.append((index, obj.data.decode('utf-8')))
			
				
	return split_positions

###############################################################################

@app.route('/barcodesplit', methods=['POST'])
def barcodesplit():

	logger = logging.getLogger('my.logger')
	logger.info("Ricevuta richiesta")	

	barcode_pattern = '^DOC[0-9]+$'
	barcode_compiled_pattern = re.compile(barcode_pattern)

	pages = pdf2image.convert_from_bytes(
		request.get_data(),
		dpi=400,
		grayscale=True
	)

	# Calculates split positions (page numbers)

	split_positions = calc_split_positions(
		pages, 
		pattern=barcode_compiled_pattern,
		barcode_type='CODE128'
	)

	# Split files and build return payload

	with io.BytesIO(request.get_data()) as data:	

		inputpdf = PdfFileReader(data)

		response_data = {}

		for i, element in enumerate(split_positions):
			
			(first_page, barcode) = element
			
			if i < len(split_positions)-1:
				last_page = split_positions[i+1][0]
			else:
				# For the last split position, the last page
				# is the last page of the document.
				last_page = inputpdf.numPages
						
			output = PdfFileWriter()
			
			for page in range(first_page, last_page):
				output.addPage(inputpdf.getPage(page))

			with io.BytesIO() as tmp:
				output.write(tmp)
				response_data[f"part-{i}"] = (f"{i:03}-{barcode}.pdf", tmp.getvalue(), 'application/pdf')

	# Send return payload

	m = MultipartEncoder(response_data)

	return Response(m.to_string(), mimetype=m.content_type)	

###############################################################################

@app.route('/barcodesplit2', methods=['POST'])
def barcodesplit2():

	logger = logging.getLogger('my.logger')
	logger.info("Ricevuta richiesta")	

	barcode_pattern = '^DOC[0-9]+$'
	barcode_compiled_pattern = re.compile(barcode_pattern)

	pages = pdf2image.convert_from_bytes(
		request.get_data(),
		dpi=400,
		grayscale=True
	)

	# Calculates split positions (page numbers)

	split_positions = calc_split_positions(
		pages, 
		pattern=barcode_compiled_pattern,
		barcode_type='CODE128'
	)

	# Split files and build return payload

	with io.BytesIO(request.get_data()) as data:	

		inputpdf = PdfFileReader(data)

		response_data = []

		for i, element in enumerate(split_positions):
			
			(first_page, barcode) = element
			
			if i < len(split_positions)-1:
				last_page = split_positions[i+1][0]
			else:
				# For the last split position, the last page
				# is the last page of the document.
				last_page = inputpdf.numPages
						
			output = PdfFileWriter()
			
			for page in range(first_page, last_page):
				output.addPage(inputpdf.getPage(page))

			file_metadata = {
				"filename": str(uuid.uuid4()),
				"part": i,
				"barcode": barcode
			}

			response_data.append(file_metadata)

			output.write(os.path.join(TMP_DIR, file_metadata["filename"]))


	return(response_data)

###############################################################################

def list_temp_files():

	res = []

	for filename in os.listdir(TMP_DIR):

		filepath = os.path.join(TMP_DIR, filename)
		
		if os.path.isfile(filepath):

			st = os.stat(filepath)    
			mtime = st.st_mtime
			age = (int)(time.time() - mtime)

			res.append({
				"filename": filename,
				"age": age
			})
		
	return(res)


@app.route('/test', methods=['GET'])
def test():
	return list_temp_files()

@app.route('/getfile/<filename>', methods=['GET'])
def getfile(filename):
	return send_from_directory(TMP_DIR, filename, mimetype="application/pdf")

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=port)