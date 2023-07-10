from flask import request, render_template, jsonify
import speech_recognition as sr
import os, uuid
from gtts import gTTS
from .ai_services_gtp_avatar_utils import get_gpt_response
from . import log


def gtp_avatar_ctr():
    return render_template('gtp_avatar_index.html', controls=True)

def robot_answer_ctr():
    log.append({"info": "robot answer enter"})
    try:
        # Read audio file from request
        data = request.files['audio'].read()

        # Generate a unique filename for the input file
        BASE_PATH = '/home/Admingania/portal_gain/ai_services/gtp_avatar/static/audio/'
        uuid_name =  str(uuid.uuid4())
        filename_in = BASE_PATH + uuid_name + 'in.wav'

        # Save audio file to disk
        with open(filename_in, 'wb') as f:
            f.write(data)
        log.append({"info": f"write {filename_in}"})

        # Generate a unique filename for the output file
        filename_out = BASE_PATH + uuid_name + 'out.wav'

        # Convert Opus codec to WAV format using FFmpeg
        os.system(f'ffmpeg -i {filename_in} -vn -acodec pcm_s16le -ac 1 -ar 16000 {filename_out}')
        log.append({"info": f"convert {filename_out}"})

        # Retrieve audio file from disk and transcribe it
        r = sr.Recognizer()
        with sr.AudioFile(filename_out) as source:
            audio_data = r.record(source)
            transcript = r.recognize_google(audio_data, language='es-ES')
        log.append({"info": f"recognize {filename_out}"})

        log.append({"info": f"gtp {transcript}"})
        # Use GPT-3 API to generate a response
        response_text = transcript #get_gpt_response(transcript)
        log.append({"info": f"gtp {response_text}"})


        # Convert the transcript to audio and save it as a WAV file
        tts = gTTS(text=response_text, lang='es')
        audio_filename = uuid_name + 'gen.wav'
        tts.save(BASE_PATH + audio_filename)
        log.append({"info": f"save as wave {response_text}"})

        # Return transcription and sentiment as dictionary
        response = {"uuid":uuid_name,"transcript": transcript, "bot_answer": response_text, "answer": audio_filename}
        log.append(response)

        os.remove(filename_in)
        os.remove(filename_out)

        return jsonify(response)

    except Exception as e:
        os.remove(filename_in)
        os.remove(filename_out)
        log.append({"error": f"Error while reading file: {e}"})
        return jsonify({'error': f'Error while processing audio: {e}'}), 400
