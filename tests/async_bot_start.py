# for python telegram bot from 20.0 version
from telegram.ext import ApplicationBuilder, MessageHandler, Filters

# import sys
# sys.path.append('..')

import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app_settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()
from django.conf import settings


from telegram_django_bot.routing import RouterCallbackMessageCommandHandler
from telegram_django_bot.tg_dj_bot import TG_DJ_Bot

from test_app.handlers import handle_lost_item_photo, handle_lost_item_description
from test_app.filters import PendingLostItemFilter


if __name__ == '__main__':
    bot = TG_DJ_Bot(settings.TELEGRAM_TOKEN)
    application = ApplicationBuilder().bot(bot).build()
    application.add_handler(MessageHandler(Filters.photo, handle_lost_item_photo))
    application.add_handler(MessageHandler(
        Filters.text & ~Filters.command & PendingLostItemFilter(),
        handle_lost_item_description,
    ))
    application.add_handler(RouterCallbackMessageCommandHandler())
    application.run_polling()