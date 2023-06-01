from flask import Flask, request, render_template
import os
import requests, json

translator_endpoint = 'https://api.cognitive.microsofttranslator.com'

app = Flask(__name__)

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

        detect_headers = {
            'Ocp-Apim-Subscription-Key': cog_key,
            'Ocp-Apim-Subscription-Region': cog_region,
            'Content-type': 'application/json'
        }

        detect_body = [{
            'text': text
        }]

        # Send the detect request and get response
        detect_response = requests.post(detect_url, params=detect_params, headers=detect_headers, json=detect_body)
        detect_response_data = detect_response.json()

        # Check if "language" key exists in the detect response
        if detect_response_data and isinstance(detect_response_data, list) and len(detect_response_data) > 0 and "language" in detect_response_data[0]:
            source_language = detect_response_data[0]["language"]
        else:
            source_language = "Unknown"

        # Use the Translator translate function
        translate_path = '/translate'
        translate_url = translator_endpoint + translate_path

        # Build the request
        translate_params = {
            'api-version': '3.0',
            'from': source_language,
            'to': ['en']
        }

        translate_headers = {
            'Ocp-Apim-Subscription-Key': cog_key,
            'Ocp-Apim-Subscription-Region': cog_region,
            'Content-type': 'application/json'
        }

        translate_body = [{
            'text': text
        }]

        # Send the translate request and get response
        translate_response = requests.post(translate_url, params=translate_params, headers=translate_headers, json=translate_body)
        translate_response_data = translate_response.json()

        # Check if translation exists in the translate response
        if translate_response_data and isinstance(translate_response_data, list) and len(translate_response_data) > 0 and "translations" in translate_response_data[0]:
            translation = translate_response_data[0]["translations"][0]["text"]
        else:
            translation = "Translation not available"

        translated_text = translation

        return render_template('home.html', translated_text=translated_text, lang_detected=source_language)

    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)



