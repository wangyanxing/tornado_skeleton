from __future__ import absolute_import

from ..handlers.health import HealthHandler
from ..handlers.index import IndexHandler


def get_routes():
    return [
        (r'/', IndexHandler),
        (r'/health', HealthHandler),
    ]
