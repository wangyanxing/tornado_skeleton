from tornado.testing import gen_test, AsyncTestCase

from bootcamp.models.title import Title


class TestTitle(AsyncTestCase):
    @gen_test
    def test_get(self):
        uuid = '1cf41b3d-f7ad-4238-bf08-8794cf7ae0f4'
        obj = Title.get(uuid)
        assert isinstance(obj, Title) == False

    @gen_test
    def test_to_dict(self):
        title = Title(
            id=1,
            uuid='1cf41b3d-f7ad-4238-bf08-8794cf7ae0f4',
            title_id='ABC-123',
            title='test title 1',
            video_path='test',
            file_names='test file',
            description='test des',
            video_size=1000000000,
            rate=8,
        )
        expected = {
            'uuid': '1cf41b3d-f7ad-4238-bf08-8794cf7ae0f4',
            'id': 1,
            'titleId': 'ABC-123',
            'title': 'test title 1',
            'videoPath': 'test',
            'fileNames': 'test file',
            'description': 'test des',
            'videoSize': 1000000000,
            'rate': 8,
        }
        assert title.to_dict() == expected
