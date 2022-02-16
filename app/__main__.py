import app.bot
from app import config

if __name__ == '__main__':
    bot = app.bot.Bender(config.BOT_NAME, config.API_ID, config.API_HASH, config.BOT_TOKEN)
    bot.run()
