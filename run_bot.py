import asyncio
import logging
from utils import get_reciept_by_name, get_reciept_via_id
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6219520277:AAGhYLp590nB63590WCUyI9jzRsVw1wQTTg"
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

@dispatcher.message_handler()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward received message back to the sender

    By default, message handler will handle all message types (like text, photo, sticker and etc.)
    """
    try:
        # Send copy of the received message
        await message.send_copy(chat_id=message.from_user.id)
        await message.answer(text='Current order is not exist (-_-)')
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

async def  on_startup(_):
    print(f'Bot started!')

# def main() -> None:
#     executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dispatcher, skip_updates=True, on_startup=on_startup)