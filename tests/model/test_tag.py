import uuid

from bootcamp.models.tag import Tag
from sqlalchemy.exc import IntegrityError
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestTag(BaseTestCase):
    def setUp(self):
        self.tag = Tag(
            id=1,
            uuid='1cf41b3d-f7ad-4238-bf08-8794cf7ae0f4',
            name='ABC',
        )
        super(TestTag, self).setUp()

    @gen_test
    def test_to_dict(self):
        expected = {
            'uuid': '1cf41b3d-f7ad-4238-bf08-8794cf7ae0f4',
            'name': 'ABC',
        }
        assert self.tag.to_dict() == expected

    def test_create(self):
        self.save(self.tag)
        db_tag = Tag.get(self.tag.uuid)
        self.assertIsNotNone(db_tag)

    def test_create_invalid_param(self):
        with self.assertRaises(IntegrityError):
            title = Tag(
                uuid=str(uuid.uuid4()),
                name=None,
            )
            self.save(title)
