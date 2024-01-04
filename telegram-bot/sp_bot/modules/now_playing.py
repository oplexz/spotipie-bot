import requests

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ChatAction
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler

from sp_bot import app
from sp_bot.modules.misc.cook_image import draw_image
from sp_bot.modules.db import DATABASE
from sp_bot.modules.misc.request_spotify import SPOTIFY
import logging

REG_MSG = 'You need to connect your Spotify account first. Contact me in pm and use /register command.'
USR_NAME_MSG = 'You need to add a username to start using the bot. Contact me in pm and use /name command.'
TOKEN_ERR_MSG = '''
Your spotify account is not properly linked with bot :( 
please use /unregister command in pm and /register again.
'''
BOT_URL = 't.me/{}'


async def nowPlaying(update: Update, context: CallbackContext) -> None:
    """Sends currently playing song when command /now is issued."""
    await context.bot.sendChatAction(update.message.chat_id, ChatAction.TYPING)

    try:
        tg_id = str(update.message.from_user.id)
        is_user = DATABASE.fetchData(tg_id)
        if is_user == None:
            button = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Contact in pm', url=BOT_URL.format(context.bot.username))]])
            await update.effective_message.reply_text(REG_MSG, reply_markup=button)

            return ConversationHandler.END
        elif is_user["username"] == 'User':
            button = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Contact in pm', url=BOT_URL.format(context.bot.username))]])
            await update.effective_message.reply_text(
                USR_NAME_MSG, reply_markup=button)

            return ConversationHandler.END
        elif is_user["token"] == '00000':
            button = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text='Contact in pm', url=BOT_URL.format(context.bot.username))]])
            await update.effective_message.reply_text(
                TOKEN_ERR_MSG, reply_markup=button)

            return ConversationHandler.END
        else:
            token = is_user["token"]
            r = SPOTIFY.getCurrentlyPlayingSong(token)

    except Exception as ex:
        print(ex)
        return

    try:
        photos = await context.bot.getUserProfilePhotos(tg_id, limit=1)
        pfp_url = photos['photos'][0][0]['file_id']
        file = await context.bot.getFile(pfp_url)
        pfp = requests.get(file.file_path)
    except:
        pfp = 'https://files.catbox.moe/eb9roq.png'

    try:
        res = r.json()
        if res['currently_playing_type'] == 'ad':
            response = "You're listening to ads."

        elif res['currently_playing_type'] == 'track':
            username = is_user["username"]
            image = draw_image(res, username, pfp)
            button = InlineKeyboardButton(
                text="Play on Spotify", url=res['item']['external_urls']['spotify'])

            await context.bot.send_photo(
                update.message.chat_id, image, reply_markup=InlineKeyboardMarkup([[button]]))

        else:
            response = "Not sure what you're listening to."
            await update.message.reply_text(response)
    except:
        # The user is most likely not listening to anything, but we never know...
        # or, well, I haven't really tested it yet...
        logging.exception("Got an error")
        update.message.reply_text("You are not listening to anything.")
        # await update.message.reply_text("Oops! Something went wrong. Please try again later.")


NOW_PLAYING_HANDLER = CommandHandler("now", nowPlaying)
app.add_handler(NOW_PLAYING_HANDLER)
