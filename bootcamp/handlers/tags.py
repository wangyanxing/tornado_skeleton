from __future__ import absolute_import

import urllib

from bootcamp.handlers.base import BaseHandler
from bootcamp.lib.exceptions import EntityAlreadyExistsError
from bootcamp.models.tag import Tag
from bootcamp.services.tag_service import TagService
from tornado.gen import coroutine


class TagsHandler(BaseHandler):
    @coroutine
    def get(self):
        service = TagService()

        self.set_header('Content-Type', 'application/json')

        if not self.get_argument("name", None, True):
            tags = yield service.get_all()
            self.write({"status": "ok", "tags": [tag.to_dict() for tag in tags]})
        else:
            tag_name = self.get_argument("name", None, True)
            tag = yield service.get_by_name(urllib.unquote(tag_name))
            if not tag:
                self.write({"status": "failed", "errorMessage": "Not found."})
            else:
                self.write({'status': 'ok', 'tag': tag.to_dict()})

    @coroutine
    def post(self):
        name = self.get_body_argument('name', None, True)

        tag_entity = Tag(
            name=name,
        )
        service = TagService()

        self.set_header('Content-Type', 'application/json')

        try:
            tag = yield service.create_with_entity(tag_entity)
            self.write({"status": "ok", "uuid": tag.uuid})
        except EntityAlreadyExistsError:
            self.write({"status": "failed", "errorMessage": "Tag name {} exist.".format(name)})
