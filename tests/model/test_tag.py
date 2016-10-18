from bootcamp.models.tag import Tag
from sqlalchemy.exc import IntegrityError
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestTag(BaseTestCase):
    def setUp(self):
        super(TestTag, self).setUp()
        self.tag = self.fixture_with_new_uuid('tag')

    @gen_test
    def test_to_dict(self):
        expected = {
            'uuid': self.tag.uuid,
            'name': 'Test tag',
        }
        assert self.tag.to_dict() == expected

    @gen_test
    def test_create(self):
        self.save(self.tag)
        db_tag = Tag.get(self.tag.uuid)
        self.assertIsNotNone(db_tag)

    @gen_test
    def test_create_invalid_param(self):
        with self.assertRaises(IntegrityError):
            title = self.fixture_with_new_uuid('tag_invalid')
            self.save(title)
