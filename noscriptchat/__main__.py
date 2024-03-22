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
        # bottle.app().add_hook("before_request", routes.on_request)
        # bottle.app().add_hook("after_request", routes.on_request_closed)
        bottle.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
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
