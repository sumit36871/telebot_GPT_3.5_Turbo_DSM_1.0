from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import sys
import groq
from groq import Groq


class Reference:
    '''
    A class to store previously response from the GROQ_API_KEY
    '''

    def __init__(self) -> None:
        self.response = ""


load_dotenv()
client = Groq(api_key = os.environ.get("GROQ_API_KEY"))

reference = Reference()

TOKEN = os.getenv("TOKEN")

#model name
MODEL_NAME = "mixtral-8x7b-32768"


# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)


def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = ""



@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Hi\nI am GoatBot!\Created by sumit. How can i assist you?")


@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")



@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm chatGPT Telegram bot created by sumit! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)


@dispatcher.message_handler()
async def Groq(message: types.Message):
    print(f">>> USER: \n\t{message.text}")
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "assistant", "content": reference.response}, 
            {"role": "user", "content": message.text} 
        ]
    )
    completion = response.choices[0]
    reference.response = completion.message.content
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id=message.chat.id, text=reference.response)



if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False)