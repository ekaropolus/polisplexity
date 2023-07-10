from gtts import gTTS
from flask import render_template, jsonify, request
import uuid


def lvc_vg_ctr():
    if request.method == 'POST':
        # get the text input from the HTML form
        article_title = request.form.get('article_title')
        article_body = request.form.get('article_body')

        try:
            # Generate a unique filename for the input file
            BASE_PATH = '/home/Admingania/portal_gain/ai_services/lite_voice_generation/static/audios/'
            uuid_name = "article_audio" #str(uuid.uuid4())
            filename_gen = uuid_name + 'gen.wav'

            # Converting the article text to speech using gTTS
            tts = gTTS(article_title + ' ' + article_body, lang='en')
            tts.save(BASE_PATH + filename_gen)

            return render_template('lvc_index.html', article_title=article_title, article_body=article_body, audio_file=filename_gen)

        except Exception as e:
            return jsonify({'error': f'Error: {e}'}), 400

    return render_template('lvc_index.html')