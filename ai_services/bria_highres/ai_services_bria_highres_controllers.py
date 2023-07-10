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
    payload = { # Define URL of the image to increase the resolution
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

    if code == 200:  # image uploaded for the first time
        visual_id = data.get("visual_id")

    elif code == 208:  # in case the image already uploaded
        visual_id = data.get("visual_id")

    if data.get("visual_id") is None:
        raise Exception(f"{data.get('description')}")

    return visual_id


def higRes(visual_id):
  """
  Arg:
    visual_id

  Return:
    Response object with URL to the upscaled image
  """

  headers = {
        "api_token": "512d38ca4a774b62ace87dabef92673a"
        }
  # API URL to increase the resolution of the visual_id image
  url = "https://engine.prod.bria-api.com/v1/" + visual_id + "/increase_resolution"

  query = {
      "desired_increase": "4" # Posible values are 2 or 4
      }

  response = requests.get(url, headers=headers, params=query)
  data = response.json()
  return data.get("image_res")



def bria_highres_controller():
    if request.method == 'GET':
        return render_template('bria_hr.html')

    if request.method == 'POST':
        # retrieve the Image URL to be rescaled
        img_url = request.form["img_url"]

        # Generate the visual ID from the url
        try:
            visual_id = register(img_url)

            # Generate the upscaled image from the visual_id image
            url_upscaled = higRes(visual_id)

            # Render template and image
            return render_template('bria_hr.html', img_url=img_url, url_upscaled=url_upscaled)

        except RequestException as e:
            # Handle any errors that occurred during the API call
            return "Error: {}".format(str(e))

    else:
        return render_template('bria_hr.html')
