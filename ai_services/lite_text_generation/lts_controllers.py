from flask import render_template, request, jsonify
import string
import random

def lts_tg_ctr():
    if request.method == 'POST':
        try:
            input_text = request.form['input_text']
            if input_text:
                input_text = input_text.translate(str.maketrans('aeiou', '12345'))
                letters = string.ascii_lowercase
                random_text = ''.join(random.choice(letters) for i in range(4))
                generated_text = input_text + '.' + random_text
                return render_template('lts_index.html', input_text=input_text, generated_text=generated_text)
        except Exception as e:
            return jsonify({'error': f'Error: {e}'}), 400
    return render_template('lts_index.html')




