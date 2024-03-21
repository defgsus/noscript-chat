import bottle

from noscriptchat import routes, config


bottle.run(
    host=config.HOST,
    port=config.PORT,
    debug=True,
    server="cheroot",
    numthreads=config.MAX_VISITORS,
)
