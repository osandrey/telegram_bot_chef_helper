from fastapi import FastAPI
from aiogram import types, Dispatcher, Bot
import asyncio
from aiogram import types, Dispatcher, Bot
from run_bot import dispatcher, bot, scheduler
from config import TELEGRAM_BOT_TOKEN, NGROK_TUNNEL_URL


app = FastAPI()
WEBHOOK_PATH = f"/bot/{TELEGRAM_BOT_TOKEN}"
WEBHOOK_URL = f"{NGROK_TUNNEL_URL}{WEBHOOK_PATH}"


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dispatcher)
    Bot.set_current(bot)
    await dispatcher.process_update(telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close(), bot
from config import TELEGRAM_BOT_TOKEN, NGROK_TUNNEL_URL


app = FastAPI()
WEBHOOK_PATH = f"/bot/{TELEGRAM_BOT_TOKEN}"
WEBHOOK_URL = f"{NGROK_TUNNEL_URL}{WEBHOOK_PATH}"


@app.on_event("startup")
async def on_startup():
    webhook_info = await bot.get_webhook_info()
    asyncio.create_task(scheduler())
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )


@app.post(WEBHOOK_PATH)
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dispatcher)
    Bot.set_current(bot)
    await dispatcher.process_update(telegram_update)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()