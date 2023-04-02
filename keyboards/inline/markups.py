from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


results_markup = InlineKeyboardMarkup(row_width=1)
results_markup.insert(InlineKeyboardButton(text='Natijalar', callback_data='results'))

def continue_markup(winner: str):
    markup = InlineKeyboardMarkup(row_width=1)
    if winner == 'user':
        text = "Yutishda davom etaman"
    elif winner == 'bot':
        text = 'Botni yutaman'
    else:
        text = "Yana o'ynayman"
    markup.insert(InlineKeyboardButton(text=text, callback_data='continue'))
    return markup

