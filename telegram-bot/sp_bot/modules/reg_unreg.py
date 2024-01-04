from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler

from sp_bot import app, BOT_URL
from sp_bot.modules.db import DATABASE
from sp_bot.modules.misc.request_spotify import SPOTIFY

PM_MSG = 'Contact me in pm to /register or /unregister your account.'
REG_MSG = 'Open the link below, to connect your Spotify account.'


async def register(update: Update, context: CallbackContext) -> None:
    'add new user'
    if update.effective_chat.type == update.effective_chat.PRIVATE:
        tg_id = str(update.effective_user.id)
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Register", url=SPOTIFY.getAuthUrl())]])
        await update.effective_message.reply_text(
            REG_MSG, reply_markup=button)
        return ConversationHandler.END
    else:
        # TODO: pass "register" to /start
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Register here", url=BOT_URL)]])
        await update.effective_message.reply_text(
            PM_MSG, reply_markup=button)
        return ConversationHandler.END


async def unregister(update: Update, context: CallbackContext) -> None:
    """Unregisters the user by deleting the user's data from the database."""
    if update.effective_chat.type == update.effective_chat.PRIVATE:
        tg_id = str(update.effective_user.id)
        try:
            is_user = DATABASE.fetchData(tg_id)
            if is_user == None:
                await update.message.reply_text(
                    "You haven't registered your account yet.")
                return ConversationHandler.END
            else:
                DATABASE.deleteData(tg_id)
                await update.message.reply_text("Account successfully removed.")
                return ConversationHandler.END

        except Exception as ex:
            print(ex)
            await update.effective_message.reply_text("Database Error.")
            return ConversationHandler.END
    else:
        # TODO: pass "unregister" to /start
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Unregister", url=BOT_URL)]])
        await update.effective_message.reply_text(
            PM_MSG, reply_markup=button)
        return ConversationHandler.END


REGISTER_HANDLER = CommandHandler("register", register)
UNREGISTER_HANDLER = CommandHandler("unregister", unRegister)

app.add_handler(REGISTER_HANDLER)
app.add_handler(UNREGISTER_HANDLER)
