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

        # Use the Translator detect function
        source_language = detect_language(text)

        # Use the Translator translate function
        translations = translate_text(text, source_language)

        languages = ['Spanish', 'English', 'French', 'German']  # Lista de nombres de idiomas

        return render_template('home.html', translations=translations, lang_detected=source_language, languages=languages)

    return render_template('home.html')

def translate_text(text, source_language):
    path = '/translate'
    url = translator_endpoint + path

    target_languages = ['es', 'en', 'fr', 'de']  # Lista de idiomas objetivo
    translations = []

    for target_language in target_languages:
        params = {
            'api-version': '3.0',
            'from': source_language,
            'to': [target_language]
        }

        headers = {
            'Ocp-Apim-Subscription-Key': cog_key,
            'Ocp-Apim-Subscription-Region': cog_region,
            'Content-type': 'application/json'
        }

        body = [{
            'text': text
        }]

        response = requests.post(url, params=params, headers=headers, json=body).json()

        translation = response[0]["translations"][0]["text"]
        translations.append(translation)

    return translations

def detect_language(text):
    path = '/detect'
    url = translator_endpoint + path

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

    response = requests.post(url, params=params, headers=headers, json=body).json()

    language = response[0]["language"]
    
    return language

if __name__ == "__main__":
    app.run(debug=True)

