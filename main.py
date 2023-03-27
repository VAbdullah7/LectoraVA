import openai
from rich.console import Console
from rich.prompt import Prompt

import config
import tts_helper


#TODO: - Add speak recognition
#TODO: - Add GUI
#TODO: - Hide api keys (it's convenient for the current use)
#TODO: - Better error managment
#TODO: - Support arabic voice (text to speech)
#TODO: - Some cleaning


VERSION = 0.5

# because github will detect openai's keys in the source code
# then it will be disabled
with open('key.txt', 'r') as f:
        openai.api_key = f.readline()

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

    prompt = [{"role": "system", "content": config.prompt()}]

    while True:
        print('\n')
        print('▬ ▬ ▬ ▬ ▬ ▬ ▬ ')
        user_input: str = Prompt.ask('[bold red]You')
        print('▬ ▬ ▬ ▬ ▬ ▬ ▬ ')
        print('\n')
        
        voice_activated = config.voice_activated()

        with console.status("[bold green]I'm thinking[/bold green]") as status:
            chat_response: str = get_bot_response(user_input, prompt)
            if voice_activated:
                tts_response, error = tts_helper.start_text_to_speech(chat_response)
                if error:
                    console.print(f'[red][Voice disabled]({error})[/red]')            
                    voice_activated = False

        print('▬ ▬ ▬ ▬ ▬ ▬ ▬ ')
        console.print(f'[bold][green]Lectora[/green]: {chat_response}[/bold]')
        print('▬ ▬ ▬ ▬ ▬ ▬ ▬ ')

        if voice_activated:
            error = tts_helper.finish_text_to_speech(tts_response)
            if error:
                console.print(f'[red][Voice disabled]({error})[/red]')




if __name__ == '__main__':
    main()
