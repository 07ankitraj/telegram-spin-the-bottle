from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# In-memory storage for games: chat_id -> player list
games = {}


async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name
    games.setdefault(chat_id, [])
    if user not in games[chat_id]:
        games[chat_id].append(user)
        await update.message.reply_text(f"{user} joined the game!")
    else:
        await update.message.reply_text(f"{user}, you are already in the game.")


async def leave(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user = update.effective_user.first_name
    if chat_id in games and user in games[chat_id]:
        games[chat_id].remove(user)
        await update.message.reply_text(f"{user} left the game.")


async def spin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    players = games.get(chat_id, [])
    if len(players) < 2:
        await update.message.reply_text("Need at least 2 players to spin!")
        return
    import random
    chosen = random.choice(players)
    await update.message.reply_text(f"The bottle points to: {chosen}!")

app = ApplicationBuilder().token(
    "8208906356:AAH_hzMBgaE-eyBnrH01dA6I2mp_pMoI1WI").build()
app.add_handler(CommandHandler("join", join))
app.add_handler(CommandHandler("leave", leave))
app.add_handler(CommandHandler("spin", spin))

app.run_polling()
