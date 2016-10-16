import datetime
import uuid

from bootcamp.models.title import Title
from sqlalchemy.exc import IntegrityError
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestTitle(BaseTestCase):
    def setUp(self):
        self.title = Title(
            id=1,
            uuid='1cf41b3d-f7ad-4238-bf08-8794cf7ae0f4',
            title_id='ABC-123',
            title='test title 1',
            video_path='test',
            file_names='test file',
            description='test des',
            video_size=1000000000,
            rate=8.1,
            length=100,
            published_date=datetime.date(2007, 12, 5),
        )
        super(TestTitle, self).setUp()

    @gen_test
    def test_to_dict(self):
        expected = {
            'uuid': '1cf41b3d-f7ad-4238-bf08-8794cf7ae0f4',
            'id': 1,
            'titleId': 'ABC-123',
            'title': 'test title 1',
            'videoPath': 'test',
            'fileNames': 'test file',
            'description': 'test des',
            'videoSize': 1000000000,
            'rate': 8.1,
            'length': 100,
            'publishedDate': '2007-12-05',
        }
        assert self.title.to_dict() == expected

    def test_create(self):
        self.save(self.title)
        db_title = Title.get(self.title.uuid)
        self.assertIsNotNone(db_title)

    def test_create_invalid_param(self):
        with self.assertRaises(IntegrityError):
            title = Title(
                uuid=str(uuid.uuid4()),
                title_id=None,  # Should not be None
                title='test title 1',
                video_path='test',
                file_names='test file',
                description='test des',
                video_size=1000000000,
                rate=8,
            )
            self.save(title)
