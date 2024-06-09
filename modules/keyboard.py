from aiogram.types import ReplyKeyboardRemove, \
	ReplyKeyboardMarkup, KeyboardButton, \
	InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from modules import config, db


async def admin_panel():
	newsletter = InlineKeyboardButton('📢Рассылка', callback_data = 'newsletter_admin')
	count_users = InlineKeyboardButton('👤Количество юзеров', callback_data='count_users_admin')
	back = InlineKeyboardButton('🔙Назад', callback_data='back')
	switch = InlineKeyboardButton('💡Переключатели', callback_data='switch')


	markup = InlineKeyboardMarkup().add(newsletter).add(count_users).add(switch).add(back)
	return markup

async def back():
	back = InlineKeyboardButton('🔙Назад', callback_data='back')
	markup = InlineKeyboardMarkup()
	
	return markup.add(back)

async def switch():
	meet_message = InlineKeyboardButton('💬Встречающая админ панель', callback_data='none')

	if db.check_meet_admin()[0][0] == 'True':
		meet_message_state = InlineKeyboardButton('🛑ВЫКЛ', callback_data='meet_message_off/on')
	if db.check_meet_admin()[0][0] == 'False':
		meet_message_state = InlineKeyboardButton('✅ВКЛ', callback_data='meet_message_off/on')


	new_user_message = InlineKeyboardButton('👤Уведомление о новых пользователях', callback_data='none')
	
	if db.check_new_user_admin() == 'True':
		new_user_message_state = InlineKeyboardButton('🛑ВЫКЛ', callback_data='new_user_message_off/on')
	if db.check_new_user_admin() == 'False':
		new_user_message_state = InlineKeyboardButton('✅ВКЛ', callback_data='new_user_message_off/on')



	back = InlineKeyboardButton('🔙Назад', callback_data='back')


	markup = InlineKeyboardMarkup()
	return markup.add(meet_message, meet_message_state).add(new_user_message, new_user_message_state).add(back)

