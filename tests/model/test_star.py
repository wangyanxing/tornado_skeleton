# coding=utf-8
from bootcamp.models.star import Star
from sqlalchemy.exc import IntegrityError
from tests.base_test import BaseTestCase
from tornado.testing import gen_test


class TestStar(BaseTestCase):
    def setUp(self):
        super(TestStar, self).setUp()
        self.star = self.install_fixture('star')

    @gen_test
    def test_to_dict(self):
        expected = {
            'uuid': '5b89bbf4-49a7-4ba1-ad1b-c2936861a527',
            'hiragana': u'我',
            'englishId': 'test_star',
            'name': 'Test Star',
            'pronunciation': None,
        }
        assert self.star.to_dict() == expected

    @gen_test
    def test_create(self):
        self.save(self.star)
        db_star = Star.get(self.star.uuid)
        self.assertIsNotNone(db_star)

    @gen_test
    def test_create_invalid_param(self):
        with self.assertRaises(IntegrityError):
            self.save(self.install_fixture('star_invalid'))
