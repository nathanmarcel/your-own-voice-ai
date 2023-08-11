import os
import requests
import json
import datetime
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = "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"
llm = OpenAI()

def file_exists(file_name):
    return os.path.exists(file_name)

def find_a_file(prompt):
    file_not_found = True
    while (file_not_found):
        file_name = str(input(prompt))

        if file_exists(file_name):
            file_not_found = False
            return file_name
        else:
            print(f"\nThe file '{file_name}' does not exist. Try again, smooth brain\n")

def create_new_voice():
    file_name = find_a_file('\nType the name of the voice calibration file (and include the extension) Type '
                              'exit to quit:\n')

    file_path = str('voices\\' + file_name)

    url = "https://play.ht/api/v2/cloned-voices/instant"
    files = {"sample_file": (file_name, open(file_path, "rb"), "audio/mpeg")}
    payload = {"voice_name": file_name}

    headers = {
        "accept": "application/json",
        "AUTHORIZATION": "Bearer 0e4dcc8dec4e43378dc9fc43c4c229a9",
        "X-USER-ID": "BiSxUFMCeiei1ff5eQwzcoXfTcp2"
    }

    response = requests.post(url, data=payload, files=files, headers=headers)

    print(response.text)


def list_voices():
    print('Listing available voices:\n')
    url = "https://play.ht/api/v2/cloned-voices"

    headers = {
        "accept": "application/json",
        "AUTHORIZATION": "Bearer 0e4dcc8dec4e43378dc9fc43c4c229a9",
        "X-USER-ID": "BiSxUFMCeiei1ff5eQwzcoXfTcp2"
    }

    response = requests.get(url, headers=headers)
    id = json.loads(response.text)
    num_voices = len(id)

    return id


def delete_voice():
    print('deleting a voice:')

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
        "AUTHORIZATION": "Bearer 0e4dcc8dec4e43378dc9fc43c4c229a9",
        "X-USER-ID": "BiSxUFMCeiei1ff5eQwzcoXfTcp2"
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
    print('generating text 2 job')
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
        "AUTHORIZATION": "Bearer 0e4dcc8dec4e43378dc9fc43c4c229a9",
        "X-USER-ID": "BiSxUFMCeiei1ff5eQwzcoXfTcp2"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = json.loads(response.text)
    voice_id = data['id']
    print(data['id'])
    return voice_id


def get_job(voice_id):
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


def get_mp3(voice_id):
    print('converting to mp3')

    new_url = "https://play.ht/api/v2/tts/" + voice_id + "?format=audio-mpeg"

    headers = {
        "accept": "text/audio/mpeg",
        "AUTHORIZATION": "Bearer 0e4dcc8dec4e43378dc9fc43c4c229a9",
        "X-USER-ID": "BiSxUFMCeiei1ff5eQwzcoXfTcp2"
    }

    final_response = requests.get(new_url, headers=headers)

    current_datetime = datetime.datetime.now()
    datetime_string = current_datetime.strftime("%Y-%m-%d_%H_%M_%S")
    datetime_string += ".mp3"
    # print("Current date and time:", datetime_string)

    open(datetime_string, 'wb').write(final_response.content)
    print('finished')


def main():
    # User inputs
    selected_voice = None
    while (1):
        user_key = input('\n\nEnter 1 select a voice.\nEnter 2 to create a new voice'
                             '\nEnter 3 to delete a  voice\nEnter 4 to quit'
                             '\nEnter enter to ask a new prompt.\n')

        if user_key == '1':
            selected_voice = list_and_select_voice()
        elif user_key == '2':
            create_new_voice()
        elif user_key == '3':
            delete_voice()
        elif user_key == '4':
            break
        else:
            if selected_voice == None:
                print('\nNice try, you didn\'t select a voice. I\'ll force you to:\n')
                list_and_select_voice()
            question = input('\nAsk away:\n')
            query = str(llm(question))
            print(query)
            voice_id = generate_job(selected_voice, query)
            get_job(voice_id)
            get_mp3(voice_id)



    print('exited and quitting')


if __name__ == "__main__":
    main()
