import asyncio
from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db
from states.states import GameState
from keyboards.inline.markups import continue_markup, results_markup
from keyboards.default.markups import stickers_markup


@dp.message_handler(content_types=['dice'], state=GameState.sender_user)
async def bot_echo(message: types.Message):
    user_score = int(message.dice.value)
    emoji = message.dice.emoji
    dice = await message.answer_dice(emoji=emoji)
    bot_score = dice.dice.value

    await asyncio.sleep(5)
    if bot_score and user_score:
        if bot_score > user_score:
            await message.answer(text="Men yutdim!", reply_markup=results_markup)
            await db.add_game(user_id=message.from_user.id, winner='bot')
        elif user_score > bot_score:
            await message.answer(text='Siz yutdingiz!', reply_markup=results_markup)
            await db.add_game(user_id=message.from_user.id, winner='user')
        else:
            await message.answer(text='Durrang!', reply_markup=results_markup)
            await db.add_game(user_id=message.from_user.id, winner='tie')


@dp.message_handler(commands=['results'], state='*')
async def get_results(message: types.Message, state: FSMContext):
    await state.finish()
    games = await db.select_all_games(user_id=message.from_user.id)
    user_result = 0
    bot_result = 0
    tie_result = 0
    for game in games:
        if game['winner'] == 'user':
            user_result += 1
        elif game['winner'] == 'bot':
            bot_result += 1
        else:
            tie_result += 1
    if max(user_result, bot_result, tie_result) == user_result:
        winner = 'user'
    elif max(user_result, bot_result, tie_result) == bot_result:
        winner = 'bot'
    elif max(user_result, bot_result, tie_result) == tie_result:
        winner = 'tie'
    await message.answer(text=f"Natijalar", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(text=f"{user_result} marta yutdingiz!😎\n{bot_result} marta yutqazdingiz!😌\n{tie_result} marta durrang!😉\n\nO'ynashda davom etamizmi?🤨", reply_markup=continue_markup(winner=winner))
    await GameState.results.set()

@dp.callback_query_handler(text='results', state='*')
async def get_results_in_game(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()
    games = await db.select_all_games(user_id=call.from_user.id)
    user_result = 0
    bot_result = 0
    tie_result = 0
    for game in games:
        if game['winner'] == 'user':
            user_result += 1
        elif game['winner'] == 'bot':
            bot_result += 1
        else:
            tie_result += 1
    if max(user_result, bot_result, tie_result) == user_result:
        winner = 'user'
    elif max(user_result, bot_result, tie_result) == bot_result:
        winner = 'bot'
    elif max(user_result, bot_result, tie_result) == tie_result:
        winner = 'tie'
    await call.message.answer(text=f"Natijalar", reply_markup=types.ReplyKeyboardRemove())
    await call.message.answer(text=f"{user_result} marta yutdingiz!😎\n{bot_result} marta yutqazdingiz!😌\n{tie_result} marta durrang!😉\n\nO'ynashda davom etamizmi?🤨", reply_markup=continue_markup(winner=winner))
    await GameState.results.set()

@dp.callback_query_handler(state=GameState.results)
async def continue_game(call: types.CallbackQuery):
    if call.data == 'continue':
        await call.message.answer(text="O'yinni davom ettirish uchun quyidagi stikerlardan birini menga yuboring!", reply_markup=stickers_markup)
        await GameState.sender_user.set()
