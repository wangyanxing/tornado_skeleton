from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def data_received(self, chunk):
        pass
