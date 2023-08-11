# Create your own AI assistant that sounds like whoever you like.

**All you need is a .mp3 file between 2 seconds to 1 hour of the person/character of interest speaking.**

## Instructions
- Add the voice file in the /voices/ folder (I added a couple there already as an example and to use)
- Check out the usage tab below:
- Run the main.py script
- You'll need to create the voices first before you start asking questions
- After creating the voice and selecting it, you can enter a prompt. The resulting answer will be created in an .mp3 file

## Usage
- You're going to need an [OpenAI](https://platform.openai.com/account/api-keys) key as well as a [Play.ht](https://play.ht/app/api-access) key
- Here's where you enter all that stuff
```
# TODO - OPEN_AI KEY STUFF
os.environ["OPENAI_API_KEY"] = "ENTER_YOUR_OPEN_AI_KEY_HERE"
llm = OpenAI()

# TODO - PLAY.HT STUFF
authorization_index = "Bearer ENTER_YOUR_PLAY.HT_KEY_HERE"  # Write your secret key here
user_id = "ENTER_YOUR_PLAY.HT_USER_ID_HERE"
```
