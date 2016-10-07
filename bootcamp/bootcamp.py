from clay_config import config
import tornado.ioloop
import tornado.web
import logging

from tornado.options import parse_command_line

from web.routes import get_routes

logger = logging.getLogger(__name__)


def make_app():
    return tornado.web.Application(get_routes())


def serve_web():
    parse_command_line()
    logger.info('App starting up')

    app = make_app()
    app.listen(config.get('server.port'))
    tornado.ioloop.IOLoop.current().start()
