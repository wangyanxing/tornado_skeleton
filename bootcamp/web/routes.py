from __future__ import absolute_import

from ..handlers.add_title import AddTitleHandler
from ..handlers.health import HealthHandler
from ..handlers.index import IndexHandler
from ..handlers.titles import TitlesHandler


def get_routes():
    return [
        (r'/', IndexHandler),
        (r'/health', HealthHandler),
        (r'/add_title', AddTitleHandler),
        (r'/titles', TitlesHandler),
    ]
