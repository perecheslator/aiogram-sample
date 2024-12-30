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
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from aiogram.types import InputFile 

import sqlite3, datetime, asyncio, random, time
from modules import keyboard, db, config, img

db.start_bot()
bot = Bot(token=config.TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


user_message_data = {}
SPAM_LIMIT = 5  # Максимум сообщений за период
SPAM_TIME_FRAME = 10  # Временное окно (в секундах)
BLOCK_TIME = 2  # Время блокировки (в секундах)
blocked_users = {}


ADMINS = db.admins_in_db()

async def check_spam(message: types.Message):
    
    user_id = message.from_user.id

    if db.check_repeat_ban(user_id) is not None:
        return True
    else:
        current_time = time.time()

        
        if user_id in blocked_users:
            if current_time < blocked_users[user_id]:
                return True
            else:
                del blocked_users[user_id] 

        
        if user_id not in user_message_data:
            user_message_data[user_id] = []

        
        user_message_data[user_id] = [
            timestamp for timestamp in user_message_data[user_id]
            if current_time - timestamp < SPAM_TIME_FRAME
        ]

        
        user_message_data[user_id].append(current_time)

        
        if len(user_message_data[user_id]) > SPAM_LIMIT:
            blocked_users[user_id] = current_time + BLOCK_TIME
            for admin_id in ADMINS:
                await bot.send_message(admin_id, f'хуесос спамит - <code>{message.chat.id}</code>')
            return True

        return False


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

def ref(msg):
	print(msg.text)
	try:
		a = msg.text.split(' ')
		return a[1]
	except:
		return 'ERROR REF'

@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
	if await check_spam(msg):
		return

	if db.main(msg) is None:
		if db.check_new_user_admin() == 'True':
			for admin_id in ADMINS:
				await bot.send_message(admin_id, f'Новый пользователь в боте @{msg.chat.username}')
				return True
			
		else:
			pass

	db.main(msg)
	#db.add_ref(msg.chat.id, ref(msg), msg)
	
	await msg.answer('Привет🌀')
	if msg.chat.id in ADMINS:
		if db.check_meet_admin()[0][0] == 'True':	
			await msg.answer('Выберете действие', reply_markup = await keyboard.admin_panel())
		else:
			pass


@dp.message_handler(commands=['admin'])
async def admin_panel(msg: types.Message):
	if msg.chat.id in ADMINS:
		pass
	else:
		await msg.answer('Выберете действие', reply_markup = await keyboard.admin_panel())

@dp.callback_query_handler(text = 'count_users_admin')
async def count_users_admin(call: types.CallbackQuery, state: FSMContext):    
	msg = call.message
	await msg.delete()

	if msg.chat.id in ADMINS:
		await msg.answer(db.all_count()[0][0])
	else:
		pass


@dp.callback_query_handler(text = 'newsletter_admin')
async def newsletter_admin_call(call: types.CallbackQuery, state: FSMContext):    
	msg = call.message
	await msg.delete()

	if msg.chat.id in ADMINS:

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

@dp.callback_query_handler(text = 'referal_system_off/on')
async def referal_system_oof_on_call(call: types.CallbackQuery, state: FSMContext):
	msg = call.message

	await msg.delete()

	db.change_referal_system()
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
