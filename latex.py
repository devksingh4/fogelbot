import requests
import uuid
import shutil
import re

HOST = 'https://rtex.probablyaweb.site'

def load_template():
	with open('template.tex', encoding = 'utf-8') as f:
		raw = f.read()
	# Remove any comments from the template
	cleaned = re.sub(r'%.*\n', '', raw)
	return cleaned


def render_latex(latex):
    template = load_template()
    id = str(uuid.uuid4())
    tempFit = template.replace("#CONTENT", latex)
    payload = {'code': tempFit, 'format': 'png'}
    response = requests.post(HOST + '/api/v2', data = payload)
    response.raise_for_status()
    jdata = response.json()
    if jdata['status'] != 'success':
        return None
    else:
        downloadUrl = HOST + '/api/v2/' + jdata['filename']
        response = requests.get(downloadUrl, stream = True)
        response.raise_for_status()
        with open('{}.png'.format(id), 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        return id
    