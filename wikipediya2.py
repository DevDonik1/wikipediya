import asyncio
import logging
import wikipedia
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command

wikipedia.set_lang('uz')

API_TOKEN = "API-TOKEN"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

router = Router()

@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply(
        "Assalomu alaykum! \n🌟 Men sizning savollaringizga javob berishga tayyorman.\nHar qanday ma'lumot yoki yordam kerak bo'lsa, bemalol so'rang. 😊 Sizni kutib qolaman! 🙌")


@router.message()
async def handle_message(message: types.Message):
    try:
        javob = wikipedia.summary(message.text)
        await message.answer(javob)
    except wikipedia.exceptions.DisambiguationError as e:
        await message.answer(f"Ko'p variantlar mavjud: {e.options}")
    except wikipedia.exceptions.HTTPTimeoutError:
        await message.answer("Internetga ulanib bo'lmadi, iltimos qayta urinib ko'ring.")
    except wikipedia.exceptions.PageError:
        await message.answer("Bunga oid maqola topilmadi...")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {str(e)}")

dp.include_router(router)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
