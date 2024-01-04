import importlib

from bson.objectid import ObjectId
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler

from sp_bot import LOGGER, app
from sp_bot.modules import ALL_MODULES
from sp_bot.modules.db import DATABASE
from sp_bot.modules.misc.request_spotify import SPOTIFY

START_TEXT = """
Hi {},

Follow these steps to start using the bot -
1. Use /register to connect your spotify account with this bot.
2. Open the provided link, give access to the bot & you will be redirected to bot's telegram link.
3. When you open that link you will be redirected back to telegram, click start.
4. After you see a 'successful' message use /name to set a display name (this will be displayed on the song status).

thats it! you can then share your song status using -
/now or using the inline query @spotipiebot.

use /help to get the list of commands.
"""

HELP_TEXT = """
Here's the list of commands:

/now - share currently playing song on spotify.
/name - change your username.
/unregister - to unlink your spotify account from the bot.
/register - to connect your spotify account with the bot.
@spotipiebot - share song using inline query
"""

IMPORTED = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("sp_bot.modules." + module_name)

    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception(
            "Can't have two modules with the same name! Please change one")


# /start command
async def start(update: Update, context: CallbackContext):
    """The /start command handler."""
    if update.effective_chat.type == update.effective_chat.PRIVATE:
        first_name = update.effective_user.first_name
        text = update.effective_message.text
        if len(text) <= 10:
            await update.effective_message.reply_text(
                START_TEXT.format(first_name), parse_mode=ParseMode.MARKDOWN)
        elif text.endswith('register'):
            await update.message.reply_text(
                "Use /register to connect your Spotify account.")
        elif text.endswith('username'):
            await update.message.reply_text(
                "Use /name to change your display name.")
        elif text.endswith('token'):
            await update.message.reply_text(
                "Use /unregister to unlink your account, then /register again.")
        elif text.endswith('notsure'):
            await update.message.reply_text("I'm not sure what you're listening to.")
        elif text.endswith('ads'):
            await update.message.reply_text(
                "You're listening to ads!")
        elif text.endswith('notlistening'):
            await update.message.reply_text(
                "You're not listening to anything at the moment.")
        else:
            _id = text[7:]
            try:
                codeObject = DATABASE.fetch_code(ObjectId(_id))
                _ = DATABASE.delete_code(ObjectId(_id))
            except Exception as ex:
                await update.message.reply_text(
                    "Use /register to connect your Spotify account.")
                LOGGER.exception(ex)
                return ConversationHandler.END

            if codeObject is None:
                await update.message.reply_text(
                    "Use /register to connect your Spotify account.")
            else:
                try:
                    tg_id = str(update.effective_user.id)
                    telegram_name = f"{update.effective_user.first_name} {update.effective_user.last_name}" if update.effective_user.last_name else update.effective_user.first_name

                    is_user = DATABASE.fetch_user_data(tg_id)
                    if is_user != None:
                        await update.message.reply_text(
                            "You are already registered.\n\nIf you're having issues, try unlinking your account using /unregister, and using /register again.")
                        return ConversationHandler.END
                    authcode = codeObject["authCode"]
                    refreshToken = SPOTIFY.getAccessToken(authcode)
                    if refreshToken == 'error':
                        await update.message.reply_text(
                            "Unable to authenticate. Please try /register again. If you're having issues using the bot, contact the developer.")
                        return ConversationHandler.END
                    DATABASE.add_user(name=telegram_name,
                                      telegram_id=tg_id, token=refreshToken)
                    await update.message.reply_text(
                        "Account successfully linked. Use /name to set a display name, then use /now to use the bot.")
                except:
                    LOGGER.exception(
                        "An exception occurred in start command handler")
                    await update.message.reply_text("Oops! Something went wrong. Please try again later.")
                    return ConversationHandler.END

        await update.effective_message.delete()
        return ConversationHandler.END
    else:
        await update.effective_message.reply_text("Hmm?")
        return ConversationHandler.END


# /help command
async def help(update: Update, context: CallbackContext):
    """The /help command handler."""
    if update.effective_chat.type != update.effective_chat.PRIVATE:
        await update.effective_message.reply_text("Contact me in PM to get the list of possible commands.",
                                                  reply_markup=InlineKeyboardMarkup(
                                                      [[InlineKeyboardButton(text="Help",
                                                                             url="t.me/{}?start=help".format(
                                                                                 context.bot.username))]]))
        return

    else:
        await update.effective_message.reply_text(
            HELP_TEXT, parse_mode=ParseMode.MARKDOWN)


# main
def main():
    start_handler = CommandHandler('start', start)
    help_handler = CommandHandler('help', help)

    app.add_handler(start_handler)
    app.add_handler(help_handler)

    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()
