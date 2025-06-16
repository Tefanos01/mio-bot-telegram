from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)
import asyncio
import re
import os

TOKEN = os.getenv("TOKEN")
utenti_in_attesa = {}

async def nuovo_utente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        user_id = member.id
        utenti_in_attesa[user_id] = update.effective_chat.id
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=(
                "🇮🇹 Benvenuto/a nel gruppo telegram di passaggio per far parte della nostra grande Family...\n"
                "🇬🇧 Welcome to the \"check-in\" telegram group of our great Family..."
            )
        )

async def ricevi_tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    match = re.search(r"#([A-Z0-9]+)", text.upper())
    if match and user_id in utenti_in_attesa:
        tag = match.group(1)
        url = f"https://royaleapi.com/player/{tag}"
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"🔗 Ecco il profilo del giocatore: {url}"
        )
        del utenti_in_attesa[user_id]
    elif user_id in utenti_in_attesa:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❗ Per favore, includi il tag del giocatore che inizia con # nel testo."
        )

async def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, nuovo_utente))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ricevi_tag))
    print("✅ Bot in esecuzione.")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
