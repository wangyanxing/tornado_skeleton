from __future__ import absolute_import

from ..handlers.add_star import AddStarHandler
from ..handlers.add_title import AddTitleHandler
from ..handlers.add_user import AddUserHandler
from ..handlers.health import HealthHandler
from ..handlers.index import IndexHandler
from ..handlers.stars import StarsHandler
from ..handlers.titles import TitlesHandler
from ..handlers.users import UsersHandler


def get_routes():
    return [
        (r'/', IndexHandler),
        (r'/health', HealthHandler),
        (r'/add_title', AddTitleHandler),
        (r'/titles', TitlesHandler),
        (r'/add_user', AddUserHandler),
        (r'/users', UsersHandler),
        (r'/add_star', AddStarHandler),
        (r'/stars', StarsHandler),
    ]
