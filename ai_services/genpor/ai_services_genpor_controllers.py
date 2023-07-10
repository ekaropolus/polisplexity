from flask import render_template, jsonify, request
import requests


def genpor_ctr():
    # Retrieve user inputs
    if request.method == 'POST':
        eye = request.form.get('eye')
        eyebrow = request.form.get('eyebrow')
        mouth = request.form.get('mouth')
        skin = request.form.get('skin')
        age = request.form.get('age')
        sex = request.form.get('sex')
        nose = request.form['nose']
        jaw = request.form['jaw']
        beard = request.form['beard']
        hair = request.form['hair']

        # Build DALL-E prompt
        prompt = f" A real portrait of {sex} {age} year old with {skin} skin, {eye} eyes, {eyebrow} eyebrows, {nose} nose, {mouth} mouth, {jaw} jaw, {beard} beard, and {hair} hair"
        # Send request to DALL-E API
        response = requests.post(
            'https://api.openai.com/v1/images/generations',
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {"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"}'
            },
            json={
                'model': 'image-alpha-001',
                'prompt': prompt,
                'num_images': 1,
                'size': '512x512',
                'response_format': 'url'
            }
        )

        # Retrieve image URL from response
        image_url = response.json()['data'][0]['url']
        return render_template('genpor_index.html', image_url=image_url)

    return render_template('genpor_index.html')