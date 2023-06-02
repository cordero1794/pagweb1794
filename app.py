from flask import Flask, request, render_template
import os
import requests, json

global translator_endpoint    
global cog_key    
global cog_region

try:
    cog_key = os.environ.get("SECRET_KEY")
    cog_region = os.environ.get("SECRET_REGION")      
    translator_endpoint = 'https://api.cognitive.microsofttranslator.com'   
except Exception as ex:        
    print(ex)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        # Aquí es donde procesarías el texto. Por ahora, solo devolvemos el mismo texto. 
        source_language = ''

        translated_text = translate_text(text, source_language)

        return render_template('home.html', translated_text=translated_text, lang_detected=source_language)
    
    return render_template('home.html')

# Use the Translator translate function
def translate_text(text, source_language):
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
    response = requests.post(url, params=params, headers=headers, json=body).json()

    # Parse JSON array and get translation
    translation = response[0]["translations"][0]["text"]

    return translation

if __name__ == "__main__":
    app.run(debug=True)






