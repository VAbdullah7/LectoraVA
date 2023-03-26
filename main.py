import openai
import pyttsx3 as tts
from rich.console import Console
from rich.prompt import Prompt

import config
import tts_helper



VERSION = 0.5

with open('key.txt', 'r') as f:
        openai.api_key = f.readline()

recognizer = speech_recognition.Recognizer()
mic = speech_recognition.Microphone(device_index=0)


speaker = tts.init()
voices = speaker.getProperty('voices')
speaker.setProperty('voice', voices[33].id)
speaker.setProperty('rate', 150)

console = Console()

config.setup()

def get_api_response(prompt) -> str :
    content: str = None

    try:
        response: dict = openai.ChatCompletion.create(
             model="gpt-3.5-turbo",
             messages=prompt
        )

        choices: dict = response.get('choices')[0]
        content = choices.get('message').get('content')

    except Exception as e:
        print('ERROR:', e)

    return content


def update_prompt(role: str, message: str, prompt):
    prompt.append({'role': role, 'content': message})


def get_bot_response(message: str, prompt) -> str:
    update_prompt('user', message, prompt)
    bot_response: str = get_api_response(prompt)

    if bot_response:
        update_prompt('assistant', bot_response, prompt)
    else:
        bot_response = 'Something went wrong...'

    return bot_response


def print_introduction():
    print(5*'\n')
    print('''
    
██╗      ███████╗  ██████╗ ████████╗  ██████╗  ██████╗   █████╗ 
██║      ██╔════╝ ██╔════╝ ╚══██╔══╝ ██╔═══██╗ ██╔══██╗ ██╔══██╗
██║      █████╗   ██║         ██║    ██║   ██║ ██████╔╝ ███████║
██║      ██╔══╝   ██║         ██║    ██║   ██║ ██╔══██╗ ██╔══██║
███████╗ ███████╗ ╚██████╗    ██║    ╚██████╔╝ ██║  ██║ ██║  ██║
╚══════╝ ╚══════╝  ╚═════╝    ╚═╝     ╚═════╝  ╚═╝  ╚═╝ ╚═╝  ╚═╝ 

ＹＯＵＲ   ＶＩＲＴＵＡＬ   ＡＳＳＩＳＴＡＮＴ   ＰＡＲＴＮＥＲ．                                                                                                   
''')
    print('▬ ▬ ▬ ▬ ▬ ▬ ▬ ')
    print('VERSION:', VERSION)
    print('▬ ▬ ▬ ▬ ▬ ▬ ▬ ')
    print(3*'\n')

def main():
    print_introduction()

    
    prompt = [{"role": "system", "content": "You are a helpful assistant. "}]

    while True:
        print('\n')
        print('▬ ▬ ▬ ▬ ▬ ▬ ▬ ')
        user_input: str = Prompt.ask('[bold red]You')
        print('▬ ▬ ▬ ▬ ▬ ▬ ▬ ')
        print('\n')
        
        voice_activated, realistic_voice = config.voice_activated()

        with console.status("[bold green]I'm thinking[/bold green]") as status:
            chat_response: str = get_bot_response(user_input, prompt)
            if realistic_voice:
                tts_response, error = tts_helper.start_text_to_speech(chat_response)
                if error:
                    console.print(f'[red][Realistic voice disabled]({error})[/red]')            
                    realistic_voice = False

        print('▬ ▬ ▬ ▬ ▬ ▬ ▬ ')
        console.print(f'[bold][green]Lectora[/green]: {chat_response}[/bold]')
        print('▬ ▬ ▬ ▬ ▬ ▬ ▬ ')

        if realistic_voice:
            error = tts_helper.finish_text_to_speech(tts_response)
            if error:
                console.print(f'[red][Realistic voice disabled]({error})[/red]')
                realistic_voice = False
        
        if voice_activated and not realistic_voice:
            speaker.say(chat_response)
            speaker.runAndWait()




if __name__ == '__main__':
    main()
