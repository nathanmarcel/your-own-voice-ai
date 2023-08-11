import os
import requests
import json
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = "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"
llm = OpenAI()

def main():
    question = input("What is your question?")
    text = llm(question)
    print(text)

def list_voice(voice_name):
    print('getting voice')
    url = "https://play.ht/api/v2/cloned-voices"
    headers = {
        "accept": "application/json",
        "AUTHORIZATION": "Bearer 0e4dcc8dec4e43378dc9fc43c4c229a9",
        "X-USER-ID": "BiSxUFMCeiei1ff5eQwzcoXfTcp2"
    }

    response = get_request(url, headers)
    id = json.loads(response.text)
    # print(voice_id[0]['id'])
    voice = id[0]['id']
    return voice

def create_text_2_speech_job(query, voice):
    print('generating text 2 job')
    url = "https://play.ht/api/v2/tts"

    payload = {
        "quality": "medium",
        "output_format": "mp3",
        "speed": 1,
        "sample_rate": 24000,
        "text": query,
        "voice": voice
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "AUTHORIZATION": "Bearer 0e4dcc8dec4e43378dc9fc43c4c229a9",
        "X-USER-ID": "BiSxUFMCeiei1ff5eQwzcoXfTcp2"
    }
    response = post_request(url, payload, headers)
    data = json.loads(response.text)
    voice_id = data['id']
    print(data['id'])

    return voice_id


def get_text_to_speech_data(voice_id):
    print('getting text2speech data')
    url = "https://play.ht/api/v2/tts/" + voice_id

    headers = {
        "accept": "application/json",
        "AUTHORIZATION": "Bearer 0e4dcc8dec4e43378dc9fc43c4c229a9",
        "X-USER-ID": "BiSxUFMCeiei1ff5eQwzcoXfTcp2"
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)

def convert_to_mp3(voice_id):
    print('converting to mp3')

    url = "https://play.ht/api/v2/tts/" + voice_id + "?format=audio-mpeg"

    headers = {
        "accept": "text/audio/mpeg",
        "AUTHORIZATION": "Bearer 0e4dcc8dec4e43378dc9fc43c4c229a9",
        "X-USER-ID": "BiSxUFMCeiei1ff5eQwzcoXfTcp2"
    }

    response = get_request(url, headers=headers)
    open('answer.mp3', 'wb').write(response.content)
    print('finished')

def get_request(url, headers):
    response = requests.get(url, headers=headers)
    return response

def post_request(url, payload, headers):
    response = requests.post(url, json=payload, headers=headers)
    return response




