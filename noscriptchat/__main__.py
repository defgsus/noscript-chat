import argparse

import bottle

from noscriptchat import routes, config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command", type=str, nargs="?", default="server",
        choices=["server", "mock"],
    )
    args = parser.parse_args()

    if args.command == "server":
        bottle.run(
            host=config.HOST,
            port=config.PORT,
            debug=True,
            server="cheroot",
            numthreads=config.MAX_VISITORS,
        )

    elif args.command == "mock":
        from noscriptchat.mock import run_mock
        run_mock(
            host=config.HOST,
            port=config.PORT,
        )


if __name__ == "__main__":
    main()
