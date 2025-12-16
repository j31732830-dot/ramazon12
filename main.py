import asyncio
import logging
import sys

import aiogram
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from mistralai import Mistral
import os
from dotenv import load_dotenv
load_dotenv()
API = os.getenv("API")
CHAT= os.getenv("CHAT")
dp = aiogram.Dispatcher()
@dp.message(Command('start'))
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Salom, {aiogram.html.bold(message.from_user.full_name)}!")

async def Chat(h:str):
    with Mistral(
            api_key=CHAT,
    ) as mistral:
        res = mistral.chat.complete(model="mistral-small-latest", messages=[
            {
                "content": f"{h} uzbekcha ma`lumot yubor",
                "role": "user",
            },
        ], stream=False)

        return res.choices[0].message.content


@dp.message()
async def echo_handler(message: Message) -> None:
    global h
    try:
        h = await message.answer("🔎")
        await message.answer(f"{await Chat(message.text)}")
        await h.delete()
    except:
        await message.answer("Bunday ma'lumot topilmadi❌")
        await h.delete()


async def main() -> None:
    bot = aiogram.Bot(token=API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

