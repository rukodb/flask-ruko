from flask import current_app, _app_ctx_stack, has_request_context
from typing import Union
from werkzeug.exceptions import NotFound

from ruko import RukoClient, RDict


class RukoDB(RDict):
    def __init__(self, app=None, host=None, port=None, key_error=NotFound):
        self.proxy = self.RkProxy(app)  # type: Union[RukoClient, RukoDB.RkProxy]
        super().__init__([], self.proxy, key_error)
        if app:
            self.init_app(app, host, port)

    def init_app(self, app, host=None, port=None):
        self.proxy._set_app(app, host, port)

    def teardown(self, exception):
        self.proxy._teardown(exception)

    class RkProxy:
        def __init__(self, app):
            self._conn = None
            self._app = app

        def _new_client(self):
            app = current_app if has_request_context() else self._app
            return RukoClient(app.config['RUKO_HOST'], int(app.config['RUKO_PORT']))

        def _get_db(self):
            if not has_request_context():
                self._conn = self._new_client()
                return self._conn
            if self._conn:
                self._conn.close()
                self._conn = None
            ctx = _app_ctx_stack.top
            if not hasattr(ctx, 'rkconn'):
                ctx.rkconn = self._new_client()
            return ctx.rkconn

        def _teardown(self, _exception):
            if self._conn:
                self._conn.close()
                self._conn = None
            ctx = _app_ctx_stack.top
            if hasattr(ctx, 'rkconn'):
                ctx.rkconn.close()

        def _set_app(self, app, host=None, port=None):
            self._app = app
            app.config.setdefault('RUKO_HOST', host or '127.0.0.1')
            app.config.setdefault('RUKO_PORT', port or 8080)
            app.teardown_appcontext(self._teardown)

        def __getattr__(self, item):
            return self._get_db().__getattribute__(item)
