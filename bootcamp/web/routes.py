from __future__ import absolute_import

from ..handlers.add_title import AddTitleHandler
from ..handlers.add_user import AddUserHandler
from ..handlers.auth.login import LoginHandler
from ..handlers.health import HealthHandler
from ..handlers.index import IndexHandler
from ..handlers.stars import StarsHandler
from ..handlers.titles import TitlesHandler
from ..handlers.user import UserHandler
from ..handlers.user_like_title import UserLikeTitleHandler
from ..handlers.user_like_titles import UserLikeTitlesHandler
from ..handlers.users import UsersHandler

uuid_reg_str = r'([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})'


def get_routes():
    return [
        (r'/', IndexHandler),
        (r'/health', HealthHandler),
        (r'/add_title', AddTitleHandler),
        (r'/titles', TitlesHandler),
        (r'/add_user', AddUserHandler),
        (r'/users', UsersHandler),
        (r'/stars', StarsHandler),
        (r'/api/users', UsersHandler),
        (r'/api/users/' + uuid_reg_str, UserHandler),
        (r'/api/users/' + uuid_reg_str + r'/like_titles', UserLikeTitlesHandler),
        (r'/api/users/' + uuid_reg_str + r'/like_titles/' + uuid_reg_str, UserLikeTitleHandler),
        (r'/auth/login', LoginHandler),
    ]
