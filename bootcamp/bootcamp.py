import logging
import os
import ssl

from clay import config
from tornado import ioloop, web
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from web.routes import get_routes

logger = logging.getLogger(__name__)

settings = {
    'cookie_secret': '__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__',
    'xsrf_cookies': False,
}


def make_app():
    return web.Application(get_routes(), **settings)


def serve_web():
    parse_command_line()
    logger.info('App starting up')

    app = make_app()
    app.listen(config.get('server.port'))
    ioloop.IOLoop.current().start()
