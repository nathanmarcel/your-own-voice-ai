import requests
import json

##########################################
##########################################
# List your cloned voice
##########################################
##########################################
print('listing cloned voice')
url = "https://play.ht/api/v2/cloned-voices"

headers = {
    "accept": "application/json",
    "AUTHORIZATION": "Bearer 0e4dcc8dec4e43378dc9fc43c4c229a9",
    "X-USER-ID": "BiSxUFMCeiei1ff5eQwzcoXfTcp2"
}

response = requests.get(url, headers=headers)
id = json.loads(response.text)
#print(voice_id[0]['id'])
voice = id[2]['id']

##########################################
##########################################
# Generate audio from text
##########################################
##########################################

print('generating text 2 job')
url = "https://play.ht/api/v2/tts"

payload = {
    "quality": "medium",
    "output_format": "mp3",
    "speed": 0.2,
    "sample_rate": 9000, #24000
    "text": "Thankfully help is imminent. Sixty percent of the U-N-S-C fleet is on route to reach from existing deployments.",
    "voice": voice
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "AUTHORIZATION": "Bearer 0e4dcc8dec4e43378dc9fc43c4c229a9",
    "X-USER-ID": "BiSxUFMCeiei1ff5eQwzcoXfTcp2"
}

response = requests.post(url, json=payload, headers=headers)
data = json.loads(response.text)
voice_id = data['id']
print(data['id'])

##########################################
##########################################
# Get text to speech data
##########################################
##########################################
print('getting text2speech data')

url = "https://play.ht/api/v2/tts/" + voice_id
# print(url)

headers = {
    "accept": "application/json",
    "AUTHORIZATION": "Bearer 0e4dcc8dec4e43378dc9fc43c4c229a9",
    "X-USER-ID": "BiSxUFMCeiei1ff5eQwzcoXfTcp2"
}

response = requests.get(url, headers=headers)
data = json.loads(response.text)

##########################################
# conversion to mp3 stuff
##########################################
##########################################
print('converting to mp3')

new_url = "https://play.ht/api/v2/tts/" + voice_id + "?format=audio-mpeg"

headers = {
    "accept": "text/audio/mpeg",
    "AUTHORIZATION": "Bearer 0e4dcc8dec4e43378dc9fc43c4c229a9",
    "X-USER-ID": "BiSxUFMCeiei1ff5eQwzcoXfTcp2"
}

final_response = requests.get(new_url, headers=headers)
open('august.mp3', 'wb').write(final_response.content)
print('finished')

