from telegram.constants import ParseMode
from prettytable import PrettyTable
import requests
import json
from time import sleep
from threading import Thread
from datetime import datetime
import logging

from telegram import Update
from telegram.ext import (
    Application,
    ContextTypes,
    PicklePersistence,
    MessageHandler,
    CommandHandler
)
import asyncio
import telegram.ext.filters as filters

from dialog_flow  import dialog_flow

# Telegram Info
TOKEN_TELEGRAM = '7143912953:AAE01epAWVP0raA3k-SQKQ21zZ-GXozcofw'
CONVERT = "USD"


headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '89f39802-ce83-4b9c-87c2-4f254aa091d8',
}


def fetch_api():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    
    params = {
    'limit':'5000',
    'convert': CONVERT
    }

    while True:
        newData = []
        response = requests.get(url, headers=headers, params=params)
        results = response.json().get("data", [])
        
        for result in results:
            symbol = result["symbol"]
            price = result["quote"][CONVERT]["price"]
            fdv = result["quote"][CONVERT]["fully_diluted_market_cap"]
            marketCap = result["quote"][CONVERT]["market_cap"]
            volume = result["quote"][CONVERT]["volume_24h"]
            lastUpdated = result["last_updated"]
            newData.append({"symbol": symbol, "price" : price, "fdv" : fdv, "tradingVolume" : volume, "marketCapitalization": marketCap, "last_updated" : lastUpdated})

        with open('data.json', 'w') as file:
            json.dump(newData, file)
        print(f'{datetime.now().strftime("%H:%M:%S")} API data updated')
        sleep(60)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # dialogflow combination
    inputData = update.message.text.removeprefix("/")
    inputData = inputData.replace("marketcap", "market cap")
    # inputData = inputData.replace("fdv", "market cap fdv")
    # inputData = inputData.replace("fully diluted market cap", "market cap fdv")

    tokenName, intent = dialog_flow(inputData)
    if tokenName:
        try:
            with open('data.json', 'r') as file:
                results = json.load(file)
                for result in results:
                    if result["symbol"] == (tokenName).upper():
                        await update.message.reply_text(f"The {intent} of {tokenName} is {result[intent]} {CONVERT}", parse_mode=ParseMode.MARKDOWN)
                        break
        except:
            pass

async def command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    inputData = update.message.text.removeprefix("/")
    inputData = inputData.replace("marketcap", "market cap")
    # inputData = inputData.replace("fdv", "market cap fdv")
    # inputData = inputData.replace("fully diluted market cap", "market cap fdv")

    tokenName, intent = dialog_flow(inputData)
    if tokenName:
        try:
            with open('data.json', 'r') as file:
                results = json.load(file)
                for result in results:
                    if result["symbol"] == (tokenName).upper():
                        await update.message.reply_text(f"The {intent} of {tokenName} is {result[intent]} {CONVERT}", parse_mode=ParseMode.MARKDOWN)
                        break
        except:
            pass

def main() -> None:
    """Run the bot."""
    # We use persistence to demonstrate how buttons can still work after the bot was restarted
    persistence = PicklePersistence(filepath="arbitrarycallbackdatabot")
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder()
        .token(TOKEN_TELEGRAM)
        .persistence(persistence)
        .arbitrary_callback_data(True)
        .build()
    )

    application.add_handler(MessageHandler(filters.Text and ~filters.COMMAND, start))
    application.add_handler(CommandHandler("price", command))
    application.add_handler(CommandHandler("fdv", command))
    application.add_handler(CommandHandler("marketcap", command))
    application.add_handler(CommandHandler("volume", command))

    # Run the bot until the user presses Ctrl-C
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    Thread(target=fetch_api).start()
    main()
    