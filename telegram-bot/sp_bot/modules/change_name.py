import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          MessageHandler, filters)

from sp_bot import BOT_URL, app
from sp_bot.modules.db import DATABASE

PM_MSG = "Contact me in PM to change your username."
REG_MSG = "You need to register first. Use /register to get started."


async def getUsername(update: Update, context: CallbackContext) -> None:
    """
    Entry point for /name command.

    Asks the user to send a username, which is then passed to `setUsername`.
    """
    if update.effective_chat.type != update.effective_chat.PRIVATE:
        # TODO: pass "name" to /start
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Change display name", url=BOT_URL)]])
        await update.effective_message.reply_text(
            PM_MSG, reply_markup=button)
        return ConversationHandler.END
    await update.effective_message.reply_text(
        "What name do you want to use? (max 15 characters)\n\nYou can use /cancel to keep your current name.")
    return USERNAME


async def setUsername(update: Update, context: CallbackContext) -> None:
    """
    Sets the username in the database.
    """
    text = update.effective_message.text.strip()
    if len(text) > 15:
        await update.message.reply_text(
            "Your name is too long. Try another one, or /cancel to keep your current name.")
        # return ConversationHandler.END
    elif text.startswith('/'):
        await update.message.reply_text(
            "You can't use commands as your name. Try another one, or /cancel to keep your current name.")
        # return ConversationHandler.END
    else:
        try:
            tg_id = str(update.message.from_user.id)
            is_user = DATABASE.fetchData(tg_id)

            if is_user == None:
                await update.message.reply_text(REG_MSG)
                return ConversationHandler.END
            else:
                DATABASE.updateData(tg_id, text)
                await update.message.reply_text(f"Username updated to {text}")
                return ConversationHandler.END

        except:
            logging.exception("An exception occurred in setUsername")
            await update.message.reply_text("Oops! Something went wrong. Please try again later.")
            return ConversationHandler.END


async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END


USERNAME = 1
USERNAME_HANDLER = ConversationHandler(
    entry_points=[CommandHandler("name", getUsername)],
    states={USERNAME: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, setUsername)]},
    fallbacks=[CommandHandler("cancel", cancel)])

app.add_handler(USERNAME_HANDLER)
