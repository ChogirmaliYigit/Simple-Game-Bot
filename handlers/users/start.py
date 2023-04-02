from aiogram import types, utils
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from data.config import ADMINS
from keyboards.default.markups import stickers_markup
from states.states import GameState


@dp.message_handler(commands=['referal'], state='*')
async def get_referal(message: types.Message, state: FSMContext):
    await state.finish()
    referals = await db.select_referals(user_id=message.from_user.id)
    bot_link = await bot.get_me()
    if referals:
        msg = 'Siz taklif qilgan foydalanuvchilar:\n\n'
        for referal in referals:
            user = await bot.get_chat(chat_id=referal[-1])
            if isinstance(user, types.Chat):
                msg += f'{referal[0]}. {user.full_name}\n'
        msg += f'\nSizning referal linkingiz: <code>https://t.me/{bot_link.username}?start={message.from_user.id}</code>'
    else:
        msg = 'Siz hali hech kimni botga taklif qilmadingiz. Marhamat referal linkingiz orqali do\'stlaringizni taklif qiling:\n\n'
        msg += f'\nSizning referal linkingiz: <code>https://t.me/{bot_link.username}?start={message.from_user.id}</code>'
    await message.answer(text=msg)

@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await state.finish()
    try:
        if message.get_args():
            user_id = int(message.get_args())
            gost_id = message.from_user.id
            referals = await db.select_referals(user_id=user_id)
            referals_ids = []
            for referal in referals:
                referals_ids.append(referal[-1])
            if gost_id not in referals_ids and gost_id != user_id:
                await db.add_referal(user_id=user_id, gost_id=gost_id)
                new_count = len(referals) + 1
                try:
                    msg = f'{message.from_user.full_name} sizning referalingiz bo\'yicha botga tashrif buyurdi.\n\n<i><b>Siz taklif qilgan jami foydalanuvchilar soni: {new_count} ta.</b></i>'
                    await bot.send_message(chat_id=user_id, text=msg)
                except utils.exceptions.CantParseEntities:
                    msg = f'Sizning referalingiz bo\'yicha yangi foydalanuvchi botga tashrif buyurdi.\n\n<i><b>Siz taklif qilgan jami foydalanuvchilar soni: {new_count} ta.</b></i>'
                    await bot.send_message(chat_id=user_id, text=msg)
                except:
                    pass
    except Exception as error:
        print(error)


    name = message.from_user.username
    user = await db.select_user(telegram_id=message.from_user.id)
    if user is None:
        user = await db.add_user(
            telegram_id=message.from_user.id,
            full_name=message.from_user.full_name,
            username=message.from_user.username,
        )
        # ADMINGA xabar beramiz
        count = await db.count_users()
        msg = f"@{user[2]} bazaga qo'shildi.\nBazada {count} ta foydalanuvchi bor."
        await bot.send_message(chat_id=ADMINS[0], text=msg)
    # user = await db.select_user(telegram_id=message.from_user.id)
    await bot.send_message(chat_id=ADMINS[0], text=f"@{name} bazaga oldin qo'shilgan")
    if name:
        await message.answer(f"Xush kelibsiz! @{name}\n\nMenga quyidagi stikerlardan birini jo'nating!", reply_markup=stickers_markup)
    else:
        await message.answer(f"Xush kelibsiz!\n\nMenga quyidagi stikerlardan birini jo'nating!", reply_markup=stickers_markup)
    await GameState.sender_user.set()