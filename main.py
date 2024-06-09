'''
						   _               _       _              
						  | |             | |     | |             
  _ __   ___ _ __ ___  ___| |__   ___  ___| | __ _| |_ ___  _ __  
 | '_ \ / _ \ '__/ _ \/ __| '_ \ / _ \/ __| |/ _` | __/ _ \| '__| 
 | |_) |  __/ | |  __/ (__| | | |  __/\__ \ | (_| | || (_) | |    
 | .__/ \___|_|  \___|\___|_| |_|\___||___/_|\__,_|\__\___/|_|    
 | |                       | |                                    
 |_|_  __ _ _ __ ___  _ __ | | ___                                
 / __|/ _` | '_ ` _ \| '_ \| |/ _ \                               
 \__ \ (_| | | | | | | |_) | |  __/                               
 |___/\__,_|_| |_| |_| .__/|_|\___|                               
					 | |                                          
					 |_|                                          
'''



import aiogram
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled

from aiogram.types import InputFile 

import sqlite3, datetime, asyncio, random
from modules import keyboard, db, config, img


bot = Bot(token=config.TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


async def anti_flood(*args, **kwargs):
	m = args[0]
	await m.answer("⚠Не так быстро!")



class Send(StatesGroup):
  msg = State()

@dp.message_handler(state=Send.msg, content_types=['text', 'photo'])
async def send_messag(message: types.Message, state: FSMContext):

	ides = db.all()

	y = 0
	n = 0

	if message.content_type == 'text':
		if message.text == '/close':
			await message.answer('Отменено⚡')
		else:

			for i in ides:
				try:
					await bot.send_message(i[0], message.text)
					y += 1
				except Exception as e:
					n += 1
					print(e)
				await message.reply(f'Отправлено \n{y} - отправлено\n{n} - Не отправлено')
	else:
		if message.text == '/close':
			await message.answer('Отменено⚡')
		else:
			for i in ides:
				try:
					await bot.send_photo(i[0], photo=message.photo[0].file_id, caption=message.caption)
					y += 1
				except:
					n += 1
			await message.reply(f'Отправлено \n{y} - отправлено\n{n} - Не отправлено')

	await state.finish()

@dp.message_handler(commands=['start'])
@dp.throttled(anti_flood,rate=0.01)
async def start(msg: types.Message):
	if db.main(msg) is None:
		if db.check_new_user_admin() == 'True':
			await bot.send_message(config.admin, f'Новый пользователь в боте @{msg.chat.username}')
		else:
			pass

	db.main(msg)
	
	await msg.answer('Привет🌀')
	if config.admin == msg.chat.id:
		if db.check_meet_admin()[0][0] == 'True':	
			await msg.answer('Выберете действие', reply_markup = await keyboard.admin_panel())
		else:
			pass


@dp.message_handler(commands=['admin'])
@dp.throttled(anti_flood,rate=0.01)
async def admin_panel(msg: types.Message):
	if config.admin != msg.chat.id:
		pass
	else:
		await msg.answer('Выберете действие', reply_markup = await keyboard.admin_panel())

@dp.callback_query_handler(text = 'count_users_admin')
async def count_users_admin(call: types.CallbackQuery, state: FSMContext):    
	msg = call.message
	await msg.delete()

	if msg.chat.id == config.admin:
		await msg.answer(db.all_count()[0][0])
	else:
		pass


@dp.callback_query_handler(text = 'newsletter_admin')
async def newsletter_admin_call(call: types.CallbackQuery, state: FSMContext):    
	msg = call.message
	await msg.delete()

	if msg.chat.id == config.admin:
		await Send.msg.set()
		await msg.answer('Введите сообщение \n\n/close для отмены')
	else:
		pass
@dp.callback_query_handler(text = 'back')
async def back_call(call: types.CallbackQuery, state: FSMContext):    
	msg = call.message

	await msg.delete()
	await start(msg)

@dp.callback_query_handler(text = 'switch')
async def switch_call(call: types.CallbackQuery, state: FSMContext):    
	msg = call.message

	await msg.delete()
	await msg.answer('Выберете действие', reply_markup=await keyboard.switch())

@dp.callback_query_handler(text = 'meet_message_off/on')
async def meet_message_oof_on_call(call: types.CallbackQuery, state: FSMContext):
	msg = call.message

	await msg.delete()

	db.change_meet_admin()
	await msg.answer('Выберете действие', reply_markup=await keyboard.switch())

@dp.callback_query_handler(text = 'new_user_message_off/on')
async def meet_message_oof_on_call(call: types.CallbackQuery, state: FSMContext):
	msg = call.message

	await msg.delete()

	db.change_new_user_admin()
	await msg.answer('Выберете действие', reply_markup=await keyboard.switch())

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)