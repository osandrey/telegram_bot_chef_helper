import asyncio
import logging

import aioschedule as aioschedule
from deep_translator import GoogleTranslator

from utils import get_reciept_by_name, get_reciept_via_id, translate
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from DB.ddl import add_users_to_db
from Postgres.ddl import create_user, get_reciept_from_db, add_view, get_most_common_reciept, get_users, \
    get_random_reciept
from config import TELEGRAM_BOT_TOKEN

# Bot token can be obtained via https://t.me/BotFather
TOKEN = TELEGRAM_BOT_TOKEN
bot = Bot(TOKEN, parse_mode="HTML")
dispatcher = Dispatcher(bot)
# All handlers should be attached to the Router (or Dispatcher)


@dispatcher.message_handler(commands=["start"])
async def command_start_handler(message: Message) -> None:
    """
    This handler receive messages with `/start` command
    """
    language = message.from_user.locale.language
    print(language)
    hello = 'Hello'
    meal_choosing = 'Please enter meal name for getting receipt of it!'

    translated_hello = GoogleTranslator(source='auto', target=language).translate(hello)
    translated_meal_choosing = GoogleTranslator(source='auto', target=language).translate(meal_choosing)
    await message.answer(f"{translated_hello}, <b>{message.from_user.full_name}!</b>\n"
                         f"{translated_meal_choosing}")
    # await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>\n"
    #                      f"Please enter meal name for getting receipt of it!")

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    last_name = message.from_user.last_name
    create_user(user_id, user_name, last_name, language)


@dispatcher.message_handler(commands=["get_meal"])
async def command_get_meal_handler(message: Message) -> None:
    """
    This handler receive messages with `/get_meal` command
    """
    language = message.from_user.locale.language
    print(language)
    hello = 'Hello'
    meal_choosing = 'Please enter meal name for getting receipt of it!'

    translated_hello = GoogleTranslator(source='auto', target=language).translate(hello)
    translated_meal_choosing = GoogleTranslator(source='auto', target=language).translate(meal_choosing)
    await message.answer(f"{translated_hello}, <b>{message.from_user.full_name}!</b>\n"
                         f"{translated_meal_choosing}")

@dispatcher.message_handler(lambda message:message.text.isalpha())
async def serch_meal_by_name(message: Message):
    list_of_meals = await get_reciept_by_name(message.text)
    meals_variation = dict()
    language = message.from_user.locale.language
    option = 1
    keyboard = InlineKeyboardMarkup(row_width=2)
    for item in list_of_meals:
        meals_variation[option] = (item.get('id'))
        # print(f'Option {option} (-_-)-> {item.get("title")}\n')
        text = item.get("title")
        translated = GoogleTranslator(source='auto', target=language).translate(text)
        button = InlineKeyboardButton(text=translated, callback_data=item.get('id'))
        keyboard.add(button)
        option += 1

    await message.answer(text='CHoose option from list: ', reply_markup=keyboard)
    # new_input = int(input('Choose option: '))
    # target_id = meals_variation[new_input]
    # title, instruction = get_reciept_via_id(target_id)


# @dispatcher.callback_query_handler()



@dispatcher.callback_query_handler()
async def catch_callback_data(call_back: types.CallbackQuery):
    # language_to_see = call_back.from_user.locale.language_name
    language = call_back.from_user.locale.language
    user_id = call_back.from_user.id
    reciept_id = call_back.data

    receipt = get_reciept_from_db(reciept_id)
    if receipt:


        title = receipt.title
        instructions = receipt.instructions
        image = receipt.image
        add_view(reciept_id)

        print('Receipt comes from DB')
    else:
        title, instructions, image = await get_reciept_via_id(reciept_id, user_id)
        print('Receipt comes from API')

    title = translate(title, language)
    instructions = translate(instructions, language)

    if len(instructions + title) < 1000:
        await bot.send_photo(chat_id=call_back.from_user.id, photo=image,caption=f'<b><i>{title}:</i></b>\n<i>{instructions}</i>')
    else:
        await bot.send_photo(chat_id=call_back.from_user.id, photo=image,
                             caption=f'<b><i>{title}:</i></b>')
        await bot.send_message(chat_id=call_back.from_user.id, text=instructions)

    return await call_back.answer('Thank you for cooperating, kindly wait ...')


@dispatcher.message_handler()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward received message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker and etc.)
    """
    try:
        # Send copy of the received message
        await message.send_copy(chat_id=message.from_user.id)
        await message.answer(text='Current order is not exist')
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

async def  on_startup(_):
    print(f'Bot started!')

# def main() -> None:
#     executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)


async def send_most_common():
    most_common_rec = get_most_common_reciept()

    users = get_users()
    print(most_common_rec.title, users)
    for user in users:
        translated_title = GoogleTranslator(target=user.language).translate(most_common_rec.title)
        translated_instruction = GoogleTranslator(target=user.language).translate(most_common_rec.instructions)

        if len(translated_instruction + translated_title) < 1000:
            await bot.send_photo(chat_id=user.id, photo=most_common_rec.image,caption=f'<b><i>{translated_title}:</i></b>\n<i>{translated_instruction}</i>')
        else:
            await bot.send_photo(chat_id=user.id, photo=most_common_rec.image,
                                 caption=f'<b><i>{translated_title}:</i></b>')
            await bot.send_message(chat_id=user.id, text=translated_instruction)


async def send_random_reciept():

    users = get_users()
    # print(reciept.title)
    for user in users:
        reciept = get_random_reciept()
        translated_title = GoogleTranslator(target=user.language).translate(reciept.title)
        translated_instruction = GoogleTranslator(target=user.language).translate(reciept.instructions)

        if len(translated_instruction + translated_title) < 1000:
            await bot.send_photo(chat_id=user.id, photo=reciept.image,caption=f'<b><i>{translated_title}:</i></b>\n<i>{translated_instruction}</i>')
        else:
            await bot.send_photo(chat_id=user.id, photo=reciept.image,
                                 caption=f'<b><i>{translated_title}:</i></b>')
            await bot.send_message(chat_id=user.id, text=translated_instruction)

async def scheduler():
    aioschedule.every().day.at("12:00").do(send_most_common)
    aioschedule.every().day.at("20:00").do(send_random_reciept)
    # aioschedule.every().minute.do(send_most_common)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)



if __name__ == "__main__":

    # asyncio.run(send_most_common())
    asyncio.run(send_random_reciept())
    # try:
    #     # logging.basicConfig(level=logging.INFO)
    #     executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
    # except Exception as error:
    #     print(f'Error name:{error}')