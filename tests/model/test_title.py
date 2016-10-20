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
            'fileNames': ['test file'],
            'stars': [
                '9f78adf8-f268-451a-bfa7-0478b6a64d47',
                '24c8cf4b-b551-4bef-95fe-30e2a6749929',
            ],
            'description': 'test des',
            'videoSize': 1000000000,
            'rate': 8.2,
            'length': 160,
            'publishedDate': '2007-12-05',
            'tags': [
                'c736b780-11b6-4190-8529-4d89504b76a0',
                'efc5907c-7316-4a36-a910-044c18e39d10',
            ],
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
