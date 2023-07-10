import time
import requests
from requests.exceptions import RequestException
from flask import request, render_template

# Translate the input text to english
def translate(text):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    # Define the headers
    headers = {
	"content-type": "application/x-www-form-urlencoded",
	"Accept-Encoding": "application/gzip",
	"X-RapidAPI-Key": "ac2667aa42mshf1d58d7dce2bd5fp10ea00jsnc025dcf7e835",
	"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }

    # Payload
    payload = "target=en&format=text&q="+text

    # Post the request
    response = requests.request("POST", url, data=payload, headers=headers)

    # Extract the response
    translated_text = response.json()['data']['translations'][0]["translatedText"]
    return translated_text


url = "https://engine.prod.bria-api.com/v1/search"
headers = {"api_token": "512d38ca4a774b62ace87dabef92673a"}

def bria_controller():
    if request.method == 'GET':
        return render_template('bria_index.html')

    if request.method == 'POST':
        # retrieve the selected options from the form
        query_text = request.form['query']
        style = request.form['style']
        atmosphere = request.form['atmosphere']
        camera = request.form['camera']
        medium = request.form['medium']


        # Translate from any language to english
        query_text = translate(query_text)

        query = {
                "query": query_text,
                "synchronous": "false",
                "gallery_search": "false",
                "num_results_per_page": "1",
                "synthetic_search": "true",
                "num_synthetic_results_per_page": "1",
                "page": "1",
                "style": style,
                "atmosphere": atmosphere,
                "camera": camera,
                "medium": medium
                }

        # Get the generated new image from Bria API
        try:
            response = requests.get(url, headers=headers, params=query)
            response.raise_for_status()  # raise an exception if the response has an HTTP error status code
            # Returns a JSON response
            imgs_url = response.json()
            # Extracting image URL from JSON response
            img_url = imgs_url['results'][0]['url']

            # Check if status code is 200
            respuesta = requests.get(img_url)
            while respuesta.status_code != 200:
                time.sleep(1)
                respuesta = requests.get(img_url)

            # Render template and image
            return render_template('bria_index.html', img_url=img_url)

        except RequestException as e:
            # Handle any errors that occurred during the API call
            return "Error: {}".format(str(e))

    else:
        return render_template('bria_index.html')
