from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          MessageHandler, filters)

from sp_bot import BOT_URL, app
from sp_bot.modules.db import DATABASE

PM_MSG = 'Contact me in pm to change your username.'
REG_MSG = 'You need to register first. use /register to get started.'


# /username command
async def getUsername(update: Update, context: CallbackContext) -> None:
    'ask user for usename'
    if update.effective_chat.type != update.effective_chat.PRIVATE:
        # TODO: pass "name" to /start
        button = InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="Change username", url=BOT_URL)]])
        await update.effective_message.reply_text(
            PM_MSG, reply_markup=button)
        return ConversationHandler.END
    await update.effective_message.reply_text(
        "Send me a username (max 15 characters)")
    return USERNAME


# username command state
async def setUsername(update: Update, context: CallbackContext) -> None:
    'save username in db'
    text = update.effective_message.text.strip()
    if len(text) > 15:
        await update.message.reply_text(
            "Invalid username. Try again using /name ")
        return ConversationHandler.END
    elif text.startswith('/'):
        await update.message.reply_text(
            "Invalid username. Try again using /name ")
        return ConversationHandler.END
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

        except Exception as ex:
            print(ex)
            await update.message.reply_text("Database Error")
            return ConversationHandler.END


async def cancel(update, context):
    await update.message.reply_text('Canceled.')
    return ConversationHandler.END


USERNAME = 1
USERNAME_HANDLER = ConversationHandler(
    entry_points=[CommandHandler('name', getUsername)],
    states={USERNAME: [MessageHandler(
            filters.TEXT & ~filters.COMMAND, setUsername)]},
    fallbacks=[CommandHandler('cancel', cancel)])

app.add_handler(USERNAME_HANDLER)
