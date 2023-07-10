from flask import render_template, request, jsonify, send_file
import random
import wave
import struct
import scipy.io.wavfile as wavfile
import numpy as np
from scipy.signal import lfilter, lfilter_zi

def lss_sg_ctr():
    if request.method == 'POST':
        try:
            audio_file = generate_sound_bel()
            return render_template('lss_index.html', audio_file = audio_file)
        except Exception as e:
            return jsonify({'error': f'Error: {e}'}), 400
    return render_template('lss_index.html')

def generate_sound_rdm(framerate,duration,amplitude):

    # Generate random sound data
    num_samples = int(framerate * duration)
    sound_data = []
    for i in range(num_samples):
        sample = random.uniform(-1, 1)
        sound_data.append(int(amplitude * sample))

    # Save the sound file to disk
    BASE_PATH = '/home/Admingania/portal_gain/ai_services/lite_sound_generation/static/audios/'
    sound_audio = 'random_sound.wav'

    sound_file = wave.open(BASE_PATH + sound_audio, 'w')
    sound_file.setparams((1, 2, framerate, num_samples, 'NONE', 'not compressed'))
    for sample in sound_data:
        sound_file.writeframes(struct.pack('h', sample))
    sound_file.close()

    return sound_audio

def generate_sound_bel():
    framerate = np.random.randint(22050, 44100)  # Choose a random framerate between 22050 and 44100 Hz
    amplitude = np.random.randint(5000, 15000)  # Choose a random amplitude between 5000 and 15000
    duration=3
    # Generate the sound waveform using the Karplus-Strong algorithm
    num_samples = int(framerate * duration)
    delay = int(framerate / 440)  # 440 Hz is A4 on the piano
    waveform = np.random.uniform(-amplitude, amplitude, delay)
    for i in range(delay, num_samples):
        sample = 0.5 * (waveform[i - delay] + waveform[i - delay - 1])
        waveform = np.append(waveform, sample)

    # Normalize the waveform and convert to 16-bit integer format
    waveform = (waveform / np.max(np.abs(waveform))) * 32767
    waveform = waveform.astype(np.int16)

    # Save the sound file to disk
    BASE_PATH = '/home/Admingania/portal_gain/ai_services/lite_sound_generation/static/audios/'
    sound_audio = 'random_sound.wav'
    wavfile.write(BASE_PATH + sound_audio, framerate, waveform)

    # Return the sound file to the client
    return sound_audio

def generate_sound_bul():
    # Set up bell model parameters
    num_modes = np.random.randint(5, 10)  # Choose a random number of modes between 5 and 10
    freqs = np.sort(np.random.uniform(500, 3000, num_modes))  # Choose random frequencies between 500 and 3000 Hz
    amps = np.random.uniform(0.1, 1.0, num_modes)  # Choose random amplitudes between 0.1 and 1.0
    decays = np.random.uniform(0.1, 0.5, num_modes)  # Choose random decay times between 0.1 and 0.5 seconds
    framerate = np.random.randint(22050, 44100)  # Choose a random framerate between 22050 and 44100 Hz
    amplitude = np.random.randint(5000, 15000)  # Choose a random amplitude between 5000 and 15000
    duration=3
    # Create a time vector
    t = np.linspace(0, duration, int(duration * framerate), endpoint=False)

    # Generate the sound waveform using modal synthesis
    waveform = np.zeros_like(t)
    for i in range(num_modes):
        b, a = np.zeros(1), np.zeros(1)
        b[0], a[0] = 1, -np.exp(-2 * np.pi * decays[i] * freqs[i])
        zi = lfilter_zi(b, a) * amps[i]
        x, _ = lfilter(b, a, np.random.randn(len(t)), zi=zi)
        waveform += x

    # Normalize the waveform and convert to 16-bit integer format
    waveform = (waveform / np.max(np.abs(waveform))) * amplitude
    waveform = waveform.astype(np.int16)

    # Save the sound file to disk
    BASE_PATH = '/home/Admingania/portal_gain/ai_services/lite_sound_generation/static/audios/'
    sound_audio = 'random_sound.wav'
    wavfile.write(BASE_PATH + sound_audio, framerate, waveform)

    # Return the sound file to the client
    return sound_audio
