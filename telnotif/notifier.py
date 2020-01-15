import logging

from telegram import error, ext, ParseMode

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class Notifier:
    def __init__(self, name, greeting, token):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.greeting = greeting

        self.updater = ext.Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher

        start_handler = ext.CommandHandler('start', self.start)
        self.dispatcher.add_handler(start_handler)

        self.dispatcher.add_error_handler(self.error_callback)

        self.updater.start_polling()

        self.registered = {}
        self.logger.info(f'started notifier for {self.name}')

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=self.greeting)
        self.registered[update.effective_chat.id] = context.bot
        self.logger.info(f'registered {update.effective_chat.id}')

    def send_message(self, message):
        for chat_id, bot in self.registered.items():
            bot.send_message(chat_id=chat_id, text=message, parse_mode=ParseMode.HTML)
        if len(self.registered) > 0:
            self.logger.info(f'sent message to {len(self.registered)} receivers')

    def error_callback(self, update, context):
        try:
            raise context.error
        except error.Unauthorized:
            # remove update.message.chat_id from conversation list
            chat_id = update.message.chat_id
            self.logger.error(f'Unauthorized: removing {chat_id} from registered list')
            del self.registered[chat_id]
        except error.BadRequest:
            # handle malformed requests - read more below!
            self.logger.error('BadRequest')
        except error.TimedOut:
            # handle slow connection problems
            self.logger.error('Timeout')
        except error.NetworkError:
            # handle other connection problems
            self.logger.error('Network error')
        except error.ChatMigrated as e:
            # the chat_id of a group has changed, use e.new_chat_id instead
            self.logger.error(f'Chat migrated: use {e.new_chat_id} now for {update.message.chat_id}')
            self.registered[e.new_chat_id] = self.registered[update.message.chat_id]
            del self.registered[update.message.chat_id]
        except error.TelegramError:
            # handle all other telegram related errors
            self.logger.error('Telegram error')


if __name__ == '__main__':
    import time
    import argparse

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--name', required=True, help='name to use for the notifier')
    arg_parser.add_argument('--greeting', required=True, help='greeting for new registerers')
    arg_parser.add_argument('--telegram-bot-token', required=True, help='token of the telegram bot')

    args = arg_parser.parse_args()

    notifier = Notifier(
        name=args.name,
        greeting=args.greeting,
        token=args.telegram_bot_token,
    )

    while True:
        notifier.send_message('Test')
        time.sleep(5)
