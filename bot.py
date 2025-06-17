from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import asyncio
import re

TOKEN = "8193058864:AAFbZmo4wVFvUcXOoVETYGngX4ExjNSMk0I"

utenti_in_attesa = {}  # {user_id: chat_id}

# Benvenuto
async def nuovo_utente(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        user_id = member.id
        utenti_in_attesa[user_id] = update.effective_chat.id

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="""🇮🇹 Benvenuto/a nel gruppo telegram di passaggio per far parte della nostra grande Family. Aiutaci a scalare le classifiche italiane e mondiali a suon di guerre tra clan💪😉   
Per favore, scrivi qua sotto il tuo nome in game e il tuo tag player, in modo da permetterci di dare un'occhiata al tuo account.

🇬🇧 Welcome to the "check-in" telegram group of our great Family. Help us climb the Italian and world rankings with clan wars💪😉 
Please, write your in-game name and your player tag, so that we can take a look at your account."""  
        )

# Messaggio contenente il tag
async def ricevi_tag(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    match = re.search(r"#([A-Z0-9]+)", text.upper())  # Cerca # seguito da testo

    if match and user_id in utenti_in_attesa:
        tag = match.group(1)  # Senza #

        url = f"https://royaleapi.com/player/{tag}"

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"🔗 Ecco il profilo del giocatore: {url}"
        )
        del utenti_in_attesa[user_id]
    elif match is None and user_id in utenti_in_attesa:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="❗ Per favore, includi il tag del giocatore che inizia con # nel testo."
        )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, nuovo_utente))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ricevi_tag))

print("Bot in esecuzione.")
app.run_polling()
