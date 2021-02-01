from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


def update(update: Update, context: CallbackContext):
    if not update.effective_message or not update.effective_user:
        return


command = CommandHandler("update", update)  # type: ignore
