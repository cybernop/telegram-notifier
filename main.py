import argparse
import logging

import telnotif

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument('--port', type=int, default=9000, help='port to listen on')
    arg_parser.add_argument('--name', required=True, help='name to use for the notifier')
    arg_parser.add_argument('--greeting', required=True, help='greeting for new registerers')
    arg_parser.add_argument('--telegram-bot-token', required=True, help='token of the telegram bot')

    args = arg_parser.parse_args()

    service = telnotif.Service(
        server_port=args.port,
        notifier_name=args.name,
        notifier_greeting=args.greeting,
        notifier_token=args.telegram_bot_token,
    )

    service.start()


if __name__ == '__main__':
    main()
