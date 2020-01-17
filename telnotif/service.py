import logging

from telnotif import server, notifier


class Service:
    def __init__(self, server_host='', server_port=9000, notifier_name='', notifier_greeting='', notifier_token=''):
        self.notifier = notifier.Notifier(notifier_name, notifier_greeting, notifier_token)
        self.server = server.Server(server_host, server_port, self.notifier)

    def start(self):
        self.server.start()


if __name__ == '__main__':
    import argparse

    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--name', required=True, help='name to use for the notifier')
    arg_parser.add_argument('--greeting', required=True, help='greeting for new registerers')
    arg_parser.add_argument('--telegram-bot-token', required=True, help='token of the telegram bot')

    args = arg_parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    service = Service(
        notifier_name=args.name,
        notifier_greeting=args.greeting,
        notifier_token=args.telegram_bot_token,
    )

    service.start()
