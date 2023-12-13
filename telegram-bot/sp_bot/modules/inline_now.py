import requests
from uuid import uuid4

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultCachedPhoto
from telegram.ext import CallbackContext, ConversationHandler, InlineQueryHandler

from sp_bot import app, TEMP_CHANNEL
from sp_bot.modules.misc.cook_image import draw_image
from sp_bot.modules.db import DATABASE
from sp_bot.modules.misc.request_spotify import SPOTIFY


async def inlineNowPlaying(update: Update, context: CallbackContext):
    'inline implementation of nowPlaying() function along with exception handeling for new users'
    try:
        tg_id = str(update.inline_query.from_user.id)
        is_user = DATABASE.fetchData(tg_id)
        if is_user == None:
            await update.inline_query.answer(
                [], switch_pm_text="You need to register first.", switch_pm_parameter='register', cache_time=0)
            return ConversationHandler.END
        elif is_user["username"] == 'User':
            await update.inline_query.answer(
                [], switch_pm_text="You need to set a username.", switch_pm_parameter='username', cache_time=0)
            return ConversationHandler.END
        elif is_user['token'] == '00000':
            await update.inline_query.answer(
                [], switch_pm_text="Registration error, please click here to fix.", switch_pm_parameter='token', cache_time=0)
            return ConversationHandler.END
        else:
            token = is_user["token"]
            r = SPOTIFY.getCurrentyPlayingSong(token)
    except Exception as ex:
        print(ex)
        return

    try:
        pfp_url = context.bot.getUserProfilePhotos(
            tg_id, limit=1)['photos'][0][0]['file_id']
        pfp = requests.get(context.bot.getFile(pfp_url).file_path)
    except:
        pfp = 'https://files.catbox.moe/eb9roq.png'

    try:
        res = r.json()
        if res['currently_playing_type'] == 'ad':
            await update.inline_query.answer(
                [], switch_pm_text="You are listening to ads.", switch_pm_parameter='ads', cache_time=0)
        elif res['currently_playing_type'] == 'track':
            username = is_user["username"]
            image = draw_image(res, username, pfp)
            button = InlineKeyboardButton(
                text="Play on Spotify", url=res['item']['external_urls']['spotify'])
            temp = await context.bot.send_photo(TEMP_CHANNEL, photo=image)
            photo = temp['photo'][1]['file_id']
            temp.delete()

            await update.inline_query.answer(
                [
                    InlineQueryResultCachedPhoto(
                        id=uuid4(),
                        photo_file_id=photo,
                        reply_markup=InlineKeyboardMarkup([[button]])
                    )
                ], cache_time=0
            )
        else:
            await update.inline_query.answer(
                [], switch_pm_text="Not sure what you're listening to.", switch_pm_parameter='notsure', cache_time=0)
    except Exception as ex:
        print(ex)
        await update.inline_query.answer([], switch_pm_text="You're not listening to anything.",
                                         switch_pm_parameter='notlistening', cache_time=0)


INLINE_QUERY_HANDLER = InlineQueryHandler(inlineNowPlaying)
app.add_handler(INLINE_QUERY_HANDLER)
