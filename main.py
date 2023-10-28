
from telegram import *
from telegram import Chat, ChatMember, ChatMemberUpdated, Update, Message
from telegram.constants import ParseMode
from telegram.ext import (
    Application,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)














def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("").build()

    # Keep track of which chats the bot is in
    application.add_handler(CommandHandler("help", help))

    # Interpret any other command or text message as a start of a private chat.
    # This will record the user as being in a private chat with bot.

    application.add_handler(MessageHandler(filters.ALL, mutecheckservice))

    # Run the bot until the user presses Ctrl-C
    # We pass 'allowed_updates' handle *all* updates including `chat_member` updates
    # To reset this, simply pass `allowed_updates=[]`
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()