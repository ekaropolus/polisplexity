import os
import uuid
from werkzeug.utils import secure_filename
from flask import url_for, jsonify
from openai import OpenAI
import requests
from PIL import Image
import base64
import json
import time

# Directory where uploaded images will be saved
UPLOAD_FOLDER = 'images/ai_ask'
# Replace '<your-api-key>' with your actual API key
stability_api_key = 'sk-sliO0V5E8H4MRRPm7fZ4Xx3IImH3xWtECrYJvs3dGtmbpsxj'

def call_openai_api(public_url):
    try:
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "What’s in this image? and how can it help the city?"},
                        {"type": "image_url", "image_url": {"url": public_url}},
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content
    except Exception as e:
        return jsonify({'error': str(e)})

def call_stability_api (image_path):
    url = "https://api.stability.ai/v2alpha/generation/image-to-video"
    data = {
        'seed': '0',
        'cfg_scale': '2.5',  # Adjust as needed
        'motion_bucket_id': '40',  # Adjust as needed
    }
    files = {
        'image': ('image.png', open(image_path, 'rb'), 'image/png'),
    }
    headers = {
        'Authorization': f'Bearer {stability_api_key}',
    }
    response = requests.post(url, data=data, files=files, headers=headers)
    return response

def save_uploaded_file(file):
    filename = str(uuid.uuid4()) + '.png'
    os.makedirs('portal_gain/static/'+ UPLOAD_FOLDER, exist_ok=True)
    file_path = os.path.join('portal_gain/static/' + UPLOAD_FOLDER, filename)
    file.save(file_path)
    return url_for('static', filename=os.path.join(UPLOAD_FOLDER, filename), _external=True), file_path

def resize_and_save_image(image_path, new_width, new_height):
    original_image = Image.open(image_path)
    resized_image = original_image.resize((new_width, new_height))
    public_url, file_path = save_uploaded_file(resized_image)
    return public_url, file_path

def call_stability_get(response_id, max_attempts=10):
    url = f"https://api.stability.ai/v2alpha/generation/image-to-video/result/{response_id}"

    headers = {
        'Authorization': f'Bearer {stability_api_key}',
        'Accept': 'application/json',
    }

    attempts = 0
    while attempts < max_attempts:
        # Make a GET request to recover the video
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            video_data_base64 = response_data.get('video')

            if video_data_base64:
                # Decode the base64 video data and save it as a binary file
                video_data_binary = base64.b64decode(video_data_base64)
                filename = str(uuid.uuid4()) + '.mp4'
                os.makedirs('portal_gain/static/'+ UPLOAD_FOLDER, exist_ok=True)
                file_path = os.path.join('portal_gain/static/' + UPLOAD_FOLDER, filename)

                with open(file_path, 'wb') as video_file:
                    video_file.write(video_data_binary)

                return response.status_code, url_for('static', filename=os.path.join(UPLOAD_FOLDER, filename), _external=True), file_path
            else:
                print("Video data not found in the response.")
        elif response.status_code == 202:
            # Video is still processing, wait for 30 seconds before checking again
            time.sleep(30)
        else:
            return response.status_code, '', ''

        attempts += 1

    # If max_attempts reached without success, return an appropriate message
    return 0, '', ''


def upload_image_util(request,city_id):
    # Check if the post request has the file part
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['image']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:  # If a file is present
        public_url, file_path = save_uploaded_file(file)

        new_width = 1024  # Replace with your desired width
        new_height = 576  # Replace with your desired heigh
        image_url, image_path = resize_and_save_image(file_path, new_width, new_height)

        # Call the OpenAI API
        ai_response = call_openai_api(public_url)

        stability_response = call_stability_api (image_path)

        if 'error' in ai_response:
            return jsonify({'error': f'open ai {ai_response}'})

        if stability_response.status_code == 200:
            stability_response_data = stability_response.json()
            # Process the Stability.ai response as needed
            response_id = stability_response_data['id']
            status_code, video_url, video_path = call_stability_get(response_id)
            if status_code != 200:
                return jsonify({'error': 'stability ai'})
        elif stability_response.status_code == 400 or 500:
            return jsonify({'error': f'stability ai {stability_response.name}'})

        return jsonify({'message': 'File uploaded and processed successfully!', 'filename': public_url, 'ai_response': ai_response, 'video_url':video_url})

    return jsonify({'error': 'Something went wrong'})
