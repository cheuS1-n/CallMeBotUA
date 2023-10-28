# IMPORTS
import logging
import yaml
from telegram import *
from telegram.ext import *

# Another python files imports
from MySQL_Driver import *
###

# IMPORT CONFIGS
with open('config.yaml', 'r') as file:
    token = yaml.safe_load(file)
    token = token['TOKEN']

###

# LOGGER SETTINGS
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


###



if __name__ == '__main__':
    if startdbs():
        application = ApplicationBuilder().token(token).build()

        start_handler = CommandHandler('sql', start)
        application.add_handler(start_handler)

        application.run_polling()

    closedbs()










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