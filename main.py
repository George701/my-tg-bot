from typing import Final
from telegram import Update
from telegram.ext import ConversationHandler, Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from os import getenv
import logging
from custom_profile import UserProfile

# logging.basicConfig(filename='my_logs.log', encoding='utf-8', filemode='w',level=logging.INFO)
logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN: Final = getenv('TOKEN')
BOT_USERNAME: Final = getenv('BOT_USERNAME')

# States
NAME, AGE = range(2)

# Dictionary to store user profiles
user_profiles = {}

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting with me! I am a bot!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am a bot, please type something so I can respond')

async def start_custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Please enter your name:')
    return NAME

async def set_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    name = update.message.text
    if user_id not in user_profiles:
        user_profiles[user_id] = UserProfile()
    user_profiles[user_id].set_profile_name(name)
    await update.message.reply_text('Please enter your age:')
    return AGE

async def set_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    age = update.message.text
    user_profiles[user_id].set_profile_age(age)
    await update.message.reply_text(f'Your profile has been set:\n{user_profiles[user_id]}')
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    print('---', processed)
    if 'hello' in processed:
        return 'Hey!'
    elif 'how are you?' in processed:
        return 'Good!'
    elif 'i love python' in processed:
        return 'Me too!'
    else:
        return 'I don\'t understand...'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)

    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    # ConversationHandler for custom_command
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('custom', start_custom_command)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_age)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    app.add_handler(conv_handler)

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling...')
    app.run_polling(poll_interval=3)