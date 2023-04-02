from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


stickers_markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
stickers_markup.insert(KeyboardButton(text='🎲'))
stickers_markup.insert(KeyboardButton(text='🎯'))
stickers_markup.insert(KeyboardButton(text='🏀'))
stickers_markup.insert(KeyboardButton(text='⚽'))
stickers_markup.insert(KeyboardButton(text='🎰'))
stickers_markup.insert(KeyboardButton(text='🎳'))