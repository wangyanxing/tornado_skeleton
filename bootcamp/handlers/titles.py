from __future__ import absolute_import

import urllib

from bootcamp.handlers.base import BaseHandler
from bootcamp.lib.exceptions import EntityAlreadyExistsError
from bootcamp.models.title import Title
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

    @coroutine
    def post(self):
        title_id = self.get_body_argument('title_id')
        title = self.get_body_argument('title')
        video_path = self.get_body_argument('video_path')
        file_names = self.get_body_argument('file_names')
        description = self.get_body_argument('description')
        maker = self.get_body_argument('maker')
        video_size = self.get_body_argument('video_size')
        rate = self.get_body_argument('rate')
        length = self.get_body_argument('length')
        published_date = self.get_body_argument('published_date')

        title_entity = Title(
            title_id=title_id,
            title=title,
            video_path=video_path,
            file_names=file_names,
            description=description,
            maker=maker,
            video_size=video_size,
            rate=rate,
            length=length,
            published_date=published_date,
        )
        service = TitleService()

        self.set_header('Content-Type', 'application/json')

        try:
            title = yield service.create_with_entity(title_entity)
            self.write({"status": "ok", "uuid": title.uuid})
        except EntityAlreadyExistsError:
            self.write({"status": "failed", "errorMessage": "Title title_id {} exist.".format(title_id)})
