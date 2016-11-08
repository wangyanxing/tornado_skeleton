from __future__ import absolute_import

from ..handlers.add_star import AddStarHandler
from ..handlers.add_tag import AddTagHandler
from ..handlers.add_title import AddTitleHandler
from ..handlers.add_user import AddUserHandler
from ..handlers.auth.login import LoginHandler
from ..handlers.health import HealthHandler
from ..handlers.index import IndexHandler
from ..handlers.star import StarHandler
from ..handlers.stars import StarsHandler
from ..handlers.tag import TagHandler
from ..handlers.tags import TagsHandler
from ..handlers.title import TitleHandler
from ..handlers.title_add_tag import TitleAddTagHandler
from ..handlers.title_tags import TitleTagsHandler
from ..handlers.titles import TitlesHandler
from ..handlers.titles_by_tag import TitlesByTagHandler
from ..handlers.titles_recent import TitlesRecentHandler
from ..handlers.user import UserHandler
from ..handlers.user_like_star import UserLikeStarHandler
from ..handlers.user_like_stars import UserLikeStarsHandler
from ..handlers.user_like_title import UserLikeTitleHandler
from ..handlers.user_like_titles import UserLikeTitlesHandler
from ..handlers.users import UsersHandler

uuid_reg_str = r'([a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})'


def get_routes():
    return [
        (r'/', IndexHandler),
        (r'/health', HealthHandler),
        (r'/add_star', AddStarHandler),
        (r'/add_tag', AddTagHandler),
        (r'/add_title', AddTitleHandler),
        (r'/titles', TitlesHandler),
        (r'/add_user', AddUserHandler),
        (r'/users', UsersHandler),
        (r'/api/stars', StarsHandler),
        (r'/api/stars/' + uuid_reg_str, StarHandler),
        (r'/api/tags', TagsHandler),
        (r'/api/tags/' + uuid_reg_str, TagHandler),
        (r'/api/titles', TitlesHandler),
        (r'/api/titles/' + uuid_reg_str, TitleHandler),
        (r'/api/titles/' + uuid_reg_str + '/add_tag/' + uuid_reg_str, TitleAddTagHandler),
        (r'/api/titles/' + uuid_reg_str + '/tags', TitleTagsHandler),
        (r'/api/titles/recent', TitlesRecentHandler),
        (r'/api/titles/tag/' + uuid_reg_str, TitlesByTagHandler),
        (r'/api/users', UsersHandler),
        (r'/api/users/' + uuid_reg_str, UserHandler),
        (r'/api/users/' + uuid_reg_str + r'/like_stars', UserLikeStarsHandler),
        (r'/api/users/' + uuid_reg_str + r'/like_stars/' + uuid_reg_str, UserLikeStarHandler),
        (r'/api/users/' + uuid_reg_str + r'/like_titles', UserLikeTitlesHandler),
        (r'/api/users/' + uuid_reg_str + r'/like_titles/' + uuid_reg_str, UserLikeTitleHandler),
        (r'/auth/login', LoginHandler),
    ]
