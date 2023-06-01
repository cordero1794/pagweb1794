from flask import Flask, request, render_template
import os
import requests, json

from flask import Flask
from flask_migrate import Migrate

app = Flask(__name__)
migrate = Migrate(app, db)

translator_endpoint = 'https://api.cognitive.microsofttranslator.com'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']

        try:
            cog_key = os.environ.get("COG_SERVICE_KEY")
            cog_region = os.environ.get("COG_SERVICE_REGION")
        except Exception as ex:
            print(ex)
            return render_template('home.html', translated_text=None, lang_detected=None, error_message="Error en las credenciales del servicio de traducción")

        # Use the Translator detect function
        detect_path = '/detect'
        detect_url = translator_endpoint + detect_path

        # Build the request
        detect_params = {
            'api-version': '3.0'
        }

from flask import Flask, request, render_template
import os
import requests, json

global translator_endpoint    
global cog_key    
global cog_region

try:
    cog_key = os.environ.get("COG_SERVICE_KEY")
    cog_region = os.environ.get("COG_SERVICE_REGION")      
    translator_endpoint = 'https://api.cognitive.microsofttranslator.com'   
except Exception as ex:        
    print(ex)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        # Aquí es donde procesarías el texto. Por ahora, solo devolvemos el mismo texto. 
        source_language = '/detect'

        translated_text = '/translate'

        return render_template('home.html', translated_text=translated_text,lang_detected=source_language)
    
    return render_template('home.html')

     # Use the Translator detect function
# Use the Translator translate function
path = '/translate'
url = translator_endpoint + path

# Build the request
params = {
    'api-version': '3.0',
    'from': source_language,
    'to': ['en']
}

headers = {
    'Ocp-Apim-Subscription-Key': cog_key,
    'Ocp-Apim-Subscription-Region': cog_region,
    'Content-type': 'application/json'
}

body = [{
    'text': text
}]

# Send the request and get response
request = requests.post(url, params=params, headers=headers, json=body)
response = request.json()

# Parse JSON array and get translation
translation = response[0]["translations"][0]["text"]



# Use the Translator detect function
path = '/detect'
url = translator_endpoint + path

# Build the request
params = {
    'api-version': '3.0'
}

headers = {
'Ocp-Apim-Subscription-Key': cog_key,
'Ocp-Apim-Subscription-Region': cog_region,
'Content-type': 'application/json'
}

body = [{
    'text': text
}]

# Send the request and get response
request = requests.post(url, params=params, headers=headers, json=body)
response = request.json()

# Parse JSON array and get language
language = response[0]["language"]

if __name__ == "__main__":
    app.run(debug=True)




