from bootcamp.models.title import Title
from sqlalchemy.exc import IntegrityError
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestTitle(BaseTestCase):
    def setUp(self):
        super(TestTitle, self).setUp()
        self.title = self.fixture_with_new_uuid('title')

    @gen_test
    def test_to_dict(self):
        expected = {
            'uuid': self.title.uuid,
            'titleId': 'ABC-123',
            'title': 'test title 1',
            'videoPath': 'test',
            'fileNames': 'test file',
            'description': 'test des',
            'videoSize': 1000000000,
            'rate': 8.2,
            'length': 160,
            'publishedDate': '2007-12-05',
        }
        assert self.title.to_dict() == expected

    def test_create(self):
        self.save(self.title)
        db_title = Title.get(self.title.uuid)
        self.assertIsNotNone(db_title)

    def test_create_invalid_param(self):
        with self.assertRaises(IntegrityError):
            title = self.fixture_with_new_uuid('title_invalid')
            self.save(title)
