import importlib

from bson.objectid import ObjectId
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler

from sp_bot import BOT_USERNAME, BOT_URL, LOGGER, app
from sp_bot.modules import ALL_MODULES
from sp_bot.modules.db import DATABASE
from sp_bot.modules.misc.request_spotify import SPOTIFY
from sp_bot.modules.registration import register, unregister

START_TEXT = """
Hi {},

To start using the bot:
1. Use /register to link your Spotify account with this bot.
2. Open the provided link, give access to the bot.
3. After you've been redirected back to the bot, click "Start".
"""

HELP_TEXT = """
Here's the list of commands:

/now — Share currently playing song
/name — Change your display name
/unregister — Unlink your Spotify account from the bot
/register — Connect your Spotify account with the bot

You can also use inline queries to share songs from Spotify — just type `@{}` in any chat, and click the image to share the song you're currently listening to!
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


async def start(update: Update, context: CallbackContext):
    """
    The /start command handler.

    Can be called manually, by clicking "Register" or "Unregister" buttons,
    or by clicking "Start" button after authenticating with Spotify.
    """
    if update.effective_chat.type == update.effective_chat.PRIVATE:
        first_name = update.effective_user.first_name
        args = context.args

        if len(args) > 0:
            args[0] = args[0].lower()

            if args[0] == 'register':
                await register(update, context)
            elif args[0] == 'unregister':
                await unregister(update, context)
            elif len(args[0]) == 24:
                _id = args[0]

                try:
                    codeObject = DATABASE.fetch_code(ObjectId(_id))
                    _ = DATABASE.delete_code(ObjectId(_id))
                except BaseException:
                    LOGGER.exception(
                        "An exception occurred in /start command handler while registering user")
                    await update.message.reply_text(
                        "Something went wrong! Try using /register again.")
                    return ConversationHandler.END

                if codeObject is None:
                    await update.message.reply_text(
                        "Something went wrong! Try using /register again.")
                else:
                    try:
                        tg_id = str(update.effective_user.id)
                        telegram_name = f"{update.effective_user.first_name} {update.effective_user.last_name}" if update.effective_user.last_name else update.effective_user.first_name

                        is_user = DATABASE.fetch_user_data(tg_id)
                        if is_user is not None:
                            await update.message.reply_text(
                                "You are already registered.\n\nIf you're having issues, try unlinking your account using /unregister, and using /register again.")
                            return ConversationHandler.END
                        authcode = codeObject["authCode"]
                        refreshToken = SPOTIFY.getAccessToken(authcode)
                        if refreshToken == 'error':
                            await update.message.reply_text("Unable to authenticate. Please try /register again. If you're having issues using the bot, contact the developer.")
                            return ConversationHandler.END
                        DATABASE.add_user(
                            name=telegram_name,
                            telegram_id=tg_id,
                            token=refreshToken)
                        await update.message.reply_text(
                            """
                            You're all set! Try using `/now` to see what you're listening to right now.
                            You can also write {} in any chat to share what you're currently listening to.
                            Use /help to see what else you can do.""")
                    except BaseException:
                        LOGGER.exception(
                            "An exception occurred in start command handler")
                        await update.message.reply_text("Oops! Something went wrong. Please try again later.")
                        return ConversationHandler.END
            else:
                await update.effective_message.reply_text(
                    START_TEXT.format(first_name), parse_mode=ParseMode.MARKDOWN)
                return ConversationHandler.END
        else:
            await update.effective_message.reply_text(
                START_TEXT.format(first_name), parse_mode=ParseMode.MARKDOWN)
            return ConversationHandler.END

        # await update.effective_message.delete()
        return ConversationHandler.END


# /help command
async def help(update: Update, context: CallbackContext):
    """The /help command handler."""
    if update.effective_chat.type != update.effective_chat.PRIVATE:
        await update.effective_message.reply_text("Contact me in PM to get the list of possible commands.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text="Help", url=BOT_URL)]]))
        return

    else:
        await update.effective_message.reply_text(HELP_TEXT.format(BOT_USERNAME), parse_mode=ParseMode.MARKDOWN)


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
