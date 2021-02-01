from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


def start_handler(update: Update, context: CallbackContext):
    if not update.effective_message or not update.effective_user:
        return
    update.effective_message.reply_text(
        f"Welcome {update.effective_user.full_name}.\n/update - To get latest update"
    )


command = CommandHandler("start", start_handler)  # type: ignore
