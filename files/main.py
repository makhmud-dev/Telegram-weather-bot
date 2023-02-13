import requests
import datetime
from config import ob_havo_Token, Bot_Token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from tranlate import to_cyrillic, to_latin



bot = Bot(token=Bot_Token)
dp = Dispatcher(bot)


def to_ascii(text):
    if text.ascii():
        return text
    else:
        return to_latin(text)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
 
	await message.reply(f"<b>Assalomu alaykum {message.from_user.first_name}! \nMen istalgan shaharning ob-havo ma\'lumotlarini bilaman\nIstalgan Shahar nomini kiriting: </b>",parse_mode='HTML')


@dp.message_handler(commands=['contact'])
async def send_contact(message: types.Message):
    text = 'bog\'lanish uchun: @makhmud_dev'
    
    message.reply(text)

@dp.message_handler()
async def get_weather(message: types.Message):
	iconka_kodlari = {
		"Clear": "Quyoshli havo \U00002600",
		"Clouds": "Bulutli havo \U00002601",
		"Rain": "Yomg'irli havo \U00002614",
		"Drizzle": "Yomg'irli havo \U00002614",
		"Thunderstorm": "Chaqmoq \U000026A1",
		"Snow": "Qor \U0001F328",
		"Mist": "Tuman \U0001F32B"
	}


	try:
		r = requests.get(
			f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={ob_havo_Token}&units=metric"
			)
		data = r.json()

		shahar = data["name"]
		harorat = data["main"]["temp"]

		ikonka = data["weather"][0]["main"]
		if ikonka in iconka_kodlari:
			sm = iconka_kodlari[ikonka]
		else:
			sm = "Bu yerdan ko'rinmayabdi :)"



		namlik = data["main"]["humidity"]
		bosim = data["main"]["pressure"]
		shamol = data["wind"]["speed"]
		quyosh_chiqishi = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
		quyosh_botishi = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
		kunning_uzunligi = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
			data["sys"]["sunrise"])


		await message.reply(f"<b>Xozirgi Vaqt Bo'yicha ({datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})\n\n"
			  f"{shahar} Shahar ob-havosi!\nHarorat: {harorat}°C  {sm}\n"
			  f"Namlik: {namlik}%\nBosim: {bosim} mm sim. ust\nShamol: {shamol} m/s\n"
			  f"Quyosh Chiqishi: {quyosh_chiqishi}\nQuyosh Botishi: {quyosh_botishi}\nKunning Uzunligi: {kunning_uzunligi}\n"
			  f"\n Salomat bo'ling! \U0001F642</b>",parse_mode='HTML'
			  )





	except:
		await message.reply('\U0001F642 Shahar nomi topilmadi \U0001F642')




if __name__ == '__main__':
	executor.start_polling(dp)
