import requests
from uuid import uuid4

from telegram import InputTextMessageContent, Update, InlineKeyboardMarkup, InlineKeyboardButton, InlineQueryResultPhoto, InlineQueryResultArticle
from telegram.ext import CallbackContext, ConversationHandler, InlineQueryHandler

from sp_bot import app, TEMP_CHANNEL, BOT_URL
from sp_bot.modules.misc.cook_image import draw_image
from sp_bot.modules.db import DATABASE
from sp_bot.modules.misc.request_spotify import SPOTIFY, InvalidGrantError
from telegram import InlineQueryResultArticle


async def inlineNowPlaying(update: Update, context: CallbackContext):
    'inline implementation of nowPlaying() function along with exception handeling for new users'
    try:
        tg_id = str(update.inline_query.from_user.id)
        is_user = DATABASE.fetchData(tg_id)
        if is_user == None:
            await update.inline_query.answer(
                [
                    InlineQueryResultArticle(
                        id=uuid4(),
                        title="Register",
                        input_message_content=InputTextMessageContent(
                            "You need to register first."),
                        reply_markup=InlineKeyboardMarkup(
                            [[InlineKeyboardButton("Register", switch_inline_query_current_chat="register")]])
                    )
                ],
                cache_time=0
            )
            return ConversationHandler.END
        elif is_user["username"] == 'User':
            await update.inline_query.answer(
                [
                    InlineQueryResultArticle(
                        id=uuid4(),
                        title="Set Username",
                        input_message_content=InputTextMessageContent(
                            "You need to set a username."),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                            "Set Username", switch_inline_query_current_chat="set_username")]])
                    )
                ],
                cache_time=0
            )
            return ConversationHandler.END
        elif is_user['token'] == '00000':
            await update.inline_query.answer(
                [
                    InlineQueryResultArticle(
                        id=uuid4(),
                        title="Registration Error",
                        input_message_content=InputTextMessageContent(
                            "Registration error, please click here to fix."),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                            "Fix Registration", switch_inline_query_current_chat="fix_registration")]])
                    )
                ],
                cache_time=0
            )
            return ConversationHandler.END
        else:
            token = is_user["token"]

            try:
                r = SPOTIFY.getCurrentlyPlayingSong(token)
            except InvalidGrantError:
                await update.inline_query.answer(
                    [
                        InlineQueryResultArticle(
                            id=uuid4(),
                            title="Your Spotify session has expired. Please log in again.",
                            input_message_content=InputTextMessageContent(
                                "Your Spotify session has expired. Please log in again."),
                            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(
                                "Login", url=BOT_URL)]])
                        )
                    ],
                    cache_time=0
                )
                return
            except Exception as e:
                print(f"An error occurred: {str(e)}")
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
            await update.inline_query.answer(
                [
                    InlineQueryResultArticle(
                        id=uuid4(),
                        title="Listening to Ads",
                        input_message_content=InputTextMessageContent(
                            "You are listening to ads.")
                    )
                ],
                cache_time=0
            )
        elif res['currently_playing_type'] == 'track':
            username = is_user["username"]
            image = draw_image(res, username, pfp)
            button = InlineKeyboardButton(
                text="Play on Spotify", url=res['item']['external_urls']['spotify'])
            temp = await context.bot.send_photo(TEMP_CHANNEL, photo=image)
            photo = temp['photo'][1]['file_id']
            await temp.delete()

            await update.inline_query.answer(
                [
                    InlineQueryResultPhoto(
                        id=uuid4(),
                        photo_url=photo,
                        thumbnail_url=photo,
                        reply_markup=InlineKeyboardMarkup([[button]])
                    )
                ],
                cache_time=0
            )
        else:
            await update.inline_query.answer(
                [
                    InlineQueryResultArticle(
                        id=uuid4(),
                        title="Unknown",
                        input_message_content=InputTextMessageContent(
                            "Not sure what you're listening to.")
                    )
                ],
                cache_time=0
            )
    except Exception as ex:
        print(ex)
        await update.inline_query.answer(
            [
                InlineQueryResultArticle(
                    id=uuid4(),
                    title="Not Listening",
                    input_message_content=InputTextMessageContent(
                        "You're not listening to anything.")
                )
            ],
            cache_time=0
        )


INLINE_QUERY_HANDLER = InlineQueryHandler(inlineNowPlaying)
app.add_handler(INLINE_QUERY_HANDLER)
