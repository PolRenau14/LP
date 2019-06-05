import requests
import gzip
import shutil

def download():
	url = 'https://github.com/jordi-petit/lp-graphbot-2019/raw/master/dades/worldcitiespop.csv.gz'
	target_path = 'worldcitiespop.csv.gz'

	response = requests.get(url, stream=True)
	if response.status_code == 200:
	    with open(target_path, 'wb') as f:
	        f.write(response.raw.read())

	with gzip.open('worldcitiespop.csv.gz', 'rb') as f_in:
	    with open('worldcitiespop.csv', 'wb') as f_out:
	        shutil.copyfileobj(f_in, f_out)

download()
