import uuid

from bootcamp.models.star import Star
from sqlalchemy.exc import IntegrityError
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestStar(BaseTestCase):
    def setUp(self):
        self.star = Star(
            id=1,
            uuid='1cf41b3d-f7ad-4238-bf08-8794cf7ae0f4',
            hiragana='ABC',
            english_id='abc',
            raw_name='abc',
        )
        super(TestStar, self).setUp()

    @gen_test
    def test_to_dict(self):
        expected = {
            'uuid': '1cf41b3d-f7ad-4238-bf08-8794cf7ae0f4',
            'hiragana': 'ABC',
            'englishId': 'abc',
            'rawName': 'abc',
            'pronunciation': None,
        }
        assert self.star.to_dict() == expected

    def test_create(self):
        self.save(self.star)
        db_star = Star.get(self.star.uuid)
        self.assertIsNotNone(db_star)

    def test_create_invalid_param(self):
        with self.assertRaises(IntegrityError):
            title = Star(
                uuid=str(uuid.uuid4()),
                hiragana=None,
                english_id=None,
                raw_name='abc',
            )
            self.save(title)
