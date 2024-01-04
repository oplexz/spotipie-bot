from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler

from sp_bot import app
from sp_bot.modules.db import DATABASE


async def statss(update: Update, context: CallbackContext):
    """
    The /statss command handler.

    Returns the number of registered users.
    """
    # TODO: check if user is admin instead
    user = str(update.message.from_user.id)
    if user in ['394012198', '259972454']:
        total_users = DATABASE.count_all()
        await update.message.reply_text(f'{total_users} Users')
    else:
        await update.effective_message.reply_text(
            "Only @neelplaysac can use this command ^-^")

    return ConversationHandler


STATS_HANDLER = CommandHandler("statss", statss)
app.add_handler(STATS_HANDLER)
