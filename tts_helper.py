import requests
import json
from playsound import playsound
import os


def text_to_speech_full(text):
    id = generate_audio(text)
    url = get_audio_url(id)
    name = download_audio(url)
    play_audio(name)

def start_text_to_speech(text):
    try:
        id = generate_audio(text)
        url = get_audio_url(id)
    except Exception as err:
        return None, err
    return url, None

def finish_text_to_speech(url):
    try:
        name = download_audio(url)
        play_audio(name)
    except Exception as err:
        return err
    return None

def generate_audio(text):
    url = "https://play.ht/api/v1/convert"
    payload = json.dumps({
        "voice": "en-US-MichelleNeural",
        "content": [text],
        'preset': 'real-time',
        'speed': 1.2
    })
    response = requests.post(url, headers=headers(), data=payload)
    return response.json()['transcriptionId']

def get_audio_url(id):
    gurl = 'https://play.ht/api/v1/articleStatus'
    param = {'transcriptionId': id}
    while True:
        response = requests.get(url=gurl, params=param, headers=headers())
        if response.json()['converted']:
            break
    return response.json()['audioUrl']

def download_audio(url):
    response = requests.get(url=url)
    name = '.voice.mp3'
    if os.path.isfile(name):
        os.remove(name)
    with open(name, 'wb') as f:
        f.write(response.content)
    return name

def headers():
    return {
      'Authorization': '28b173ee2743421fbd2d69f2c1939ece',
      'X-User-ID': 'SOr2kvrcSFYGtB3zPP3WzMFpdk02',
      'Content-Type': 'application/json'
    }

def play_audio(path):
    playsound(path)




