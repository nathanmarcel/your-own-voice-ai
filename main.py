import os
import requests
import json
import datetime
from langchain.llms import OpenAI

# TODO - OPEN_AI KEY STUFF
os.environ["OPENAI_API_KEY"] = "ENTER_YOUR_OPEN_AI_KEY_HERE"
llm = OpenAI()

# TODO - PLAY.HT STUFF
authorization_index = "Bearer ENTER_YOUR_PLAY.HT_KEY_HERE"  # Write your secret key here
user_id = "ENTER_YOUR_PLAY.HT_USER_ID_HERE"


def file_exists(file_name, folder_name):
    file_path = os.path.join(folder_name, file_name)
    return os.path.exists(file_path)


def find_a_file(prompt, folder_name):
    file_not_found = True
    while (file_not_found):
        file_name = str(input(prompt))

        if file_exists(file_name, folder_name):
            file_not_found = False
            return file_name
        else:
            print(f"\nThe file '{file_name}' does not exist. Try again, smooth brain\n")


def create_new_voice():
    file_name = find_a_file('\nOk so you\'re creating a new voice. Make sure the voice file is between 2 seconds to '
                            'an hour, and that it is stored in the /voices/ folder. '
                            'Type the name of the voice calibration file (and include the extension):\n', 'voices')

    file_path = str('voices\\' + file_name)
    no_extension = os.path.splitext(file_name)[0]

    url = "https://play.ht/api/v2/cloned-voices/instant"
    files = {"sample_file": (file_name, open(file_path, "rb"), "audio/mpeg")}
    payload = {"voice_name": no_extension}

    headers = {
        "accept": "application/json",
        "AUTHORIZATION": authorization_index,
        "X-USER-ID": user_id
    }

    response = requests.post(url, data=payload, files=files, headers=headers)

    print(response.text)


def list_voices():
    print('\nListing available voices:\n')
    url = "https://play.ht/api/v2/cloned-voices"

    headers = {
        "accept": "application/json",
        "AUTHORIZATION": authorization_index,
        "X-USER-ID": user_id
    }

    response = requests.get(url, headers=headers)
    return json.loads(response.text)


def delete_voice():
    print('\nOk so you are deleting a voice.')
    id = list_voices()
    num_voices = len(id)
    voice_not_found = True

    while (voice_not_found):
        for i in range(num_voices):
            print(id[i]['name'])

        voice_to_be_deleted = input('\nEnter the name of the voice you want to delete:\n')

        for j in range(num_voices):
            voice_name = id[j]['name']
            if voice_name == voice_to_be_deleted:
                voice_not_found = False
                deleted_voice_id = id[j]['id']
        if (voice_not_found):
            print('\n Yeah, that voice name doesn\'t exist. Try again moron')

    url = "https://play.ht/api/v2/cloned-voices/"

    payload = {"voice_id": deleted_voice_id}
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "AUTHORIZATION": authorization_index,
        "X-USER-ID": user_id
    }

    response = requests.delete(url, json=payload, headers=headers)
    print(response.text)


def list_and_select_voice():
    id = list_voices()
    num_voices = len(id)

    while (1):
        for i in range(num_voices):
            print(id[i]['name'])

        voice_to_be_selected = input('\nEnter the name of the voice you want to select:\n')

        for j in range(num_voices):
            voice_name = id[j]['name']
            if voice_name == voice_to_be_selected:
                return id[j]['id']
        print('\n Yeah, that voice does\'t exist. Try again bud.\n')


def generate_job(voice, prompt):
    url = "https://play.ht/api/v2/tts"

    payload = {
        "quality": "medium",
        "output_format": "mp3",
        "speed": 0.2,
        "sample_rate": 9000,  # 24000
        "text": prompt,
        "voice": voice
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "AUTHORIZATION": authorization_index,
        "X-USER-ID": user_id
    }

    response = requests.post(url, json=payload, headers=headers)
    data = json.loads(response.text)
    return data['id']


def get_job(voice_id):
    url = "https://play.ht/api/v2/tts/" + voice_id
    headers = {
        "accept": "application/json",
        "AUTHORIZATION": authorization_index,
        "X-USER-ID": user_id
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.text)


def get_mp3(voice_id):
    print('\nCreating your .mp3 response. If this takes a long time you better have asked a good question\n')

    new_url = "https://play.ht/api/v2/tts/" + voice_id + "?format=audio-mpeg"

    headers = {
        "accept": "text/audio/mpeg",
        "AUTHORIZATION": authorization_index,
        "X-USER-ID": user_id
    }

    final_response = requests.get(new_url, headers=headers)
    current_datetime = datetime.datetime.now()
    datetime_string = current_datetime.strftime("%Y-%m-%d_%H_%M_%S")
    datetime_string += ".mp3"

    open(datetime_string, 'wb').write(final_response.content)
    print('\nFinished. Your filename is: ' + datetime_string)


def main():
    selected_voice = None
    while (1):
        user_key = input('\n\nEnter 1 select a voice.\nEnter 2 to create a new voice'
                         '\nEnter 3 to delete a  voice\nEnter 4 to quit'
                         '\nEnter anything else to ask a new prompt.\n')

        if user_key == '1':
            selected_voice = list_and_select_voice()
        elif user_key == '2':
            create_new_voice()
        elif user_key == '3':
            delete_voice()
        elif user_key == '4':
            break
        else:
            if selected_voice is None:
                print('\nNice try, you didn\'t select a voice. I\'ll force you to:\n')
                list_and_select_voice()
            question = input('\nAsk away:\n')
            query = str(llm(question))
            print(query)
            voice_id = generate_job(selected_voice, query)
            get_job(voice_id)
            get_mp3(voice_id)

    print('\nYou chose to quit. Quitters never win in life.\n')


if __name__ == "__main__":
    main()
