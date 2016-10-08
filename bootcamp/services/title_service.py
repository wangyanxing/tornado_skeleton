import uuid

from bootcamp.lib.string import make_unicode
from bootcamp.models.title import Title
from bootcamp.services import logger
from bootcamp.services.datastores.title_store import TitleStore


class TitleService(object):
    def __init__(self):
        self.store = TitleStore()

    def create_title_with_entity(self, title_entity):
        if not title_entity.uuid:
            title_entity.uuid = str(uuid.uuid4())
        title_entity.validate()

        title = self.store.create_from_entity(title_entity)
        logger.info(
            dict(
                uuid=title.uuid,
                title_id=title.title_id,
                method='create_title_with_entity',
            )
        )
        self.handle_title_added(title)
        return title

    def handle_title_added(self, title):
        pass

    def create_title_with_dict(self, title_info):
        title = make_unicode(title_info.get('title'))
        video_path = make_unicode(title_info.get('video_path'))
        file_names = make_unicode(title_info.get('file_names'))
        description = make_unicode(title_info.get('description'))
        title_uuid = uuid.uuid4()

        title = Title({
            'uuid': title_uuid,
            'title_id': title_info.get('title_id'),
            'title': title,
            'video_path': video_path,
            'file_names': file_names,
            'description': description,
            'video_size': title_info.get('video_size'),
            'rate': title_info.get('rate'),
        })
        return self.create_title_with_entity(title)

    def get_title(self, title_uuid):
        return self.store.get_title(title_uuid)

    def get_titles(self):
        return self.store.get_titles()
