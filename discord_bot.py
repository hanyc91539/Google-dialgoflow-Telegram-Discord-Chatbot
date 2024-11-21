from discord import Intents, Embed, Color
from discord.ext import tasks, commands
from datetime import datetime
from time import sleep
import json
from dialog_flow import dialog_flow

TOKEN = 'MTE4NzA2MjExNTc5NDY4MTg5OQ.G9qrOl.bK-xdv4L9P7Xye4g-VTH07BA1DGPvD2Nl6T7m4'

CHANNEL_ID = 1219314677142781952

bot = commands.Bot(command_prefix='!', intents=Intents.all())

@bot.event
async def on_message(message):
    template = '''"The {intent} of {tokenName} is {value} USD"'''

    content = str(message.content)
    
    inputData = content.removeprefix("/")
    inputData = inputData.replace("marketcap", "market cap")
    # inputData = inputData.replace("fdv", "market cap fdv")
    # inputData = inputData.replace("fully diluted market cap", "market cap fdv")

    tokenName, intent = dialog_flow(inputData)
    if tokenName:
        channel = bot.get_channel(CHANNEL_ID)

        if channel:
            try:
                with open(f'data.json', 'r') as file:
                    results = json.load(file)
                    for result in results:
                        if result["symbol"] == content.removeprefix("/").upper():
                            await channel.send(template.format(intent=intent, tokenName=tokenName, value=result[intent]))
                            ok = True
                            break
            except:
                pass
        else:
            pass


if __name__ == "__main__":
    bot.run(TOKEN)
