import os
import inspect
import importlib
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from flask import Flask as _Flask, make_response, jsonify, g, request
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from src.bases.error import HTTPError
from src.common.utils import log_data

from .resource import Resource


class Flask(_Flask):
    redis = None


class Factory(object):
    def __init__(self,
                 config,
                 redis=None,
                 resource_module=None,
                 error_handler=None,
                 request_callback=None,
                 response_callback=None):

        self.config = config
        self.resource_module = resource_module
        self.error_handler = error_handler
        self.request_callback = request_callback
        self.response_callback = response_callback
        self.redis = redis

    @staticmethod
    def default_error_handler(app):
        @app.errorhandler(Exception)
        def handle_error(e):
            if isinstance(e, (HTTPError, )):
                status_code = e.status_code
                data = e.output()
            elif isinstance(e, HTTPException):
                status_code = e.code
                data = e.__class__.__name__
            else:
                status_code = 500
                if app.debug:
                    raise e
                data = dict(message='Server error - %s' % e)
            if status_code >= 500:
                sentry_sdk.capture_exception(e)

            return make_response(jsonify(data), status_code)

    def install_resource(self, app):
        if not self.resource_module:
            return

        resource_classes = set()
        rs_root_pack = self.resource_module.__name__.split('.')
        rs_root_dir = os.path.dirname(self.resource_module.__file__)
        for dir_path, dir_names, file_names in os.walk(rs_root_dir):
            diff = os.path.relpath(dir_path, rs_root_dir)
            if diff == '.':
                diff_dirs = []
            else:
                diff_dirs = diff.split('/')
            target_pack_prefix = rs_root_pack + diff_dirs
            for dir_name in dir_names:
                target_pack = target_pack_prefix + [dir_name]
                module = importlib.import_module('.'.join(target_pack))
                classes = inspect.getmembers(module,
                                             inspect.isclass)
                for cls_name, cls in classes:
                    resource_classes.add(cls)

        for cls in resource_classes:
            if not issubclass(cls, Resource):
                continue

            # ignore resources those have none endpoint attr
            if not cls.endpoint:
                continue

            endpoint = cls.endpoint
            if cls.endpoint_prefix:
                endpoint = cls.endpoint_prefix + endpoint
            app.add_url_rule(endpoint,
                             view_func=cls.as_view(cls.__name__))

    def add_plugin(self, app):
        app.redis = self.redis

    def create_app(self):
        app = Flask(__name__)

        '''Cross origin'''
        CORS(app, supports_credentials=True,
             automatic_options=True)

        '''Load config'''
        app.config.from_object(self.config)

        '''Error handling configuration'''
        error_handler = self.error_handler or self.default_error_handler
        error_handler(app)

        '''Callbacks configuration'''

        @app.before_request
        def handle_before_request():
            self.log_request()
            g.redis = self.redis

        @app.after_request
        def handle_after_request(response):
            response.headers['Content-Type'] = 'application/json'
            return response

        '''Resources installation'''
        self.install_resource(app)

        '''Add plugins'''
        self.add_plugin(app)

        if hasattr(self.config, 'SENTRY_DNS'):
            '''Setup sentry'''
            sentry_sdk.init(
                dsn=self.config.SENTRY_DNS,
                environment=self.config.ENV,
                integrations=[FlaskIntegration()]
            )

        return app

    def log_request(self):
        pattern = 'RECEIVED REQUEST - {path} - {payload}'

        payload = dict(
            agrs=request.args.to_dict(),
            json=request.json,
            form=request.form.to_dict()
        )

        log_data(
            mode='info',
            template=pattern,
            kwargs=dict(
                path=request.path,
                payload=payload
            )
        )
