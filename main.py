from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, Poll
from responses import get_response

# get token
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
MENTION: Final[str] = os.getenv('BOT_MENTION')

# bot setup
intents: Intents = Intents.default()
# intents.message_content = True # on = have access to all messages, off = only mentions
client: Client = Client(intents=intents)


# respond to messages
async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Message read failed")  # this is fine if message_content is False
        return

    # cut the '?' out of the string if a user sends a private message
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    # remove the mention
    if user_message.startswith(MENTION):
        user_message = user_message.removeprefix(MENTION).strip()

    try:
        response: str = get_response(user_message)
        print(response)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print("An Unexpected Fuck Has Occurred:", e)


# bot login confirmation
@client.event
async def on_ready() -> None:
    print(f'Successfully logged in as {client.user}')


# read messages
@client.event
async def on_message(message: Message) -> None:
    # stop the psycho from talking to itself
    if message.author == client.user:
        return

    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}" ')

    await send_message(message, user_message)


# main, logon
def main() -> None:
    client.run(token=TOKEN)


if __name__ == "__main__":
    main()
