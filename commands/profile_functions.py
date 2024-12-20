from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters, ContextTypes
from profile.custom_profile import UserProfile  # Абсолютный импорт класса UserProfile


# Dictionary to store user profiles
user_profiles = {}

# States
NAME, AGE = range(2)

async def get_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Here will be info about profile')

async def start_set_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Как я могу к вам обращаться?')
    return NAME

async def set_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    name = update.message.text
    if user_id not in user_profiles:
        user_profiles[user_id] = UserProfile(user_id)
    user_profiles[user_id].set_profile_name(name)
    await update.message.reply_text('Сколько вам полных лет?')
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

def get_conversation_handler():
    return ConversationHandler(
        entry_points=[CommandHandler('setprofile', start_set_profile)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_name)],
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_age)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )