from __future__ import absolute_import

import urllib

from bootcamp.handlers.base import BaseHandler
# from bootcamp.lib.exceptions import EntityAlreadyExistsError
# from bootcamp.models.title import Title
from bootcamp.services.title_service import TitleService
from tornado.gen import coroutine


class TitlesHandler(BaseHandler):
    @coroutine
    def get(self):
        service = TitleService()

        self.set_header('Content-Type', 'application/json')

        if not self.get_argument("id", None, True):
            titles = yield service.get_all()
            self.write({"status": "ok", "titles": [title.to_dict() for title in titles]})
        else:
            title_id = self.get_argument("id", None, True)
            title = yield service.get_by_id(urllib.unquote(title_id))
            if not title:
                self.write({"status": "failed", "errorMessage": "Not found."})
            else:
                self.write({'status': 'ok', 'title': title.to_dict()})
