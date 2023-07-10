import requests
from flask import request, render_template
from requests.exceptions import RequestException


def register(image_url):
    """
    Arg:
        URL of the image to be registered

    Return:
        The visual ID of the image
    """

    # API URL to register
    url = "https://engine.prod.bria-api.com/v1/register"
    payload = { # Define URL of the image to recast
        "image_url": image_url,
        "is_private": True
          }

    headers = {
    "Content-Type": "application/json",
    "api_token": "512d38ca4a774b62ace87dabef92673a"
      }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    code = data.get('code')

    visual_id = data.get("visual_id")

    if code == 200:  # image uploaded for the first time
        visual_id = data.get("visual_id")

    elif code == 208:  # in case the image already uploaded
        visual_id = data.get("visual_id")

    if visual_id is None:
        raise Exception(f"{data.get('description')}")

    return visual_id


def recast(visual_id, profession):
    """
    Arg:
    visual_id

    Return:
    Response object with image URL to the recast
    """

    headers = {
        "api_token": "512d38ca4a774b62ace87dabef92673a"
        }
    # API URL to create customized and eye-catching images of the visual_id image
    url = "https://engine.prod.bria-api.com/v1/" + visual_id + "/recast_model"

    query = {
        "prompt": profession
        }

    response = requests.post(url, headers=headers, params=query)
    data = response.json()
    return data.get("image_res")


################################################################

def bria_recast_controller():
    if request.method == 'GET':
        return render_template('bria_recast.html')

    if request.method == 'POST':
        # Get the image url from the request
        img_url = request.form["img_url"]
        profession = request.form["profession"]

        # Generate the visual ID from the url
        try:
            visual_id = register(img_url)

            # Generate the recast of the image from the visual_id image
            url_recast = recast(visual_id, profession)

            # Render template and image
            return render_template('bria_recast.html', img_url=img_url, url_recast=url_recast)

        except RequestException as e:
            # Handle any errors that occurred during the API call
            return "Error: {}".format(str(e))

    else:
        return render_template('bria_recast.html')
