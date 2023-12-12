from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler

from sp_bot import dispatcher
from sp_bot.modules.db import DATABASE


def statss(update: Update, context: CallbackContext):
    'returns the number of registered users, devs only'
    user = str(update.message.from_user.id)
    if user in ['394012198', '259972454']:
        total_users = DATABASE.countAll()
        update.message.reply_text(f'{total_users} Users')
    else:
        update.effective_message.reply_text(
            "Only @neelplaysac can use this command ^-^")

    return ConversationHandler


STATS_HANDLER = CommandHandler("statss", statss)
dispatcher.add_handler(STATS_HANDLER)
