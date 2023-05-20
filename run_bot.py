import asyncio
import logging
from utils import get_reciept_by_name, get_reciept_via_id, translate
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from DB.ddl import add_users_to_db
from Postgres.ddl import create_user, get_reciept_from_db, add_view
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
    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>\n"
                         f"Please enter meal name for getting receipt of it!")

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    last_name = message.from_user.last_name
    create_user(user_id, user_name, last_name)

@dispatcher.message_handler(commands=["get_meal"])
async def command_get_meal_handler(message: Message) -> None:
    """
    This handler receive messages with `/get_meal` command
    """

    await message.answer(f"Hello, <b>{message.from_user.full_name}!</b>\n"
                         f"Please enter meal name for getting receipt of it!")

@dispatcher.message_handler(lambda message:message.text.isalpha())
async def serch_meal_by_name(message: Message):
    list_of_meals = await get_reciept_by_name(message.text)
    meals_variation = dict()
    option = 1
    keyboard = InlineKeyboardMarkup(row_width=2)
    for item in list_of_meals:
        meals_variation[option] = (item.get('id'))
        # print(f'Option {option} (-_-)-> {item.get("title")}\n')
        button = InlineKeyboardButton(text=item.get("title"), callback_data=item.get('id'))
        keyboard.add(button)
        option += 1

    await message.answer(text='CHoose option from list: ', reply_markup=keyboard)
    # new_input = int(input('Choose option: '))
    # target_id = meals_variation[new_input]
    # title, instruction = get_reciept_via_id(target_id)


@dispatcher.callback_query_handler()
async def catch_callback_data(call_back: types.CallbackQuery):
    language_to_see = call_back.from_user.locale.language_name
    language = call_back.from_user.locale.language
    print(language)
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


if __name__ == "__main__":
    pass
    # try:
    #     # logging.basicConfig(level=logging.INFO)
    #     executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)
    # except Exception as error:
    #     print(f'Error name:{error}')