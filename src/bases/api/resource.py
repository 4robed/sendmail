import inspect
import importlib
import json
from datetime import datetime
from bson import ObjectId
from flask import (request, current_app as app, g, make_response,
                   send_file, redirect)
from flask.views import View

from src.common.constants import HTTP_METHODS
from src.bases.error import (HTTPError, )

from .method_handler import MethodHandler


class CustomJsonEncoder(json.JSONEncoder):
    def default(self, o: any) -> any:
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, ObjectId):
            return str(o)
        return super(CustomJsonEncoder, self).default(o)


class MetaResource(type):
    def __init__(cls, name, bases, attrs):
        super(MetaResource, cls).__init__(name, bases, attrs)

        # the 'methods' module must be defined in the resource directory,
        # all method handler classes must be defined in this module
        methods_module_path = cls.__module__ + '.methods'
        try:
            methods_module = importlib.import_module(methods_module_path)
        except ModuleNotFoundError:
            methods_module = None

        if not methods_module:
            return

        method_handlers = attrs.get('method_handlers', {})

        classes = inspect.getmembers(methods_module,
                                     inspect.isclass)

        for cls_name, _class in classes:
            if not issubclass(_class, MethodHandler):
                continue
            if cls_name.upper() not in HTTP_METHODS:
                continue
            method_handlers[cls_name.upper()] = _class

        cls.method_handlers = method_handlers

        # handle endpoint prefixes
        prefixes = []
        for base in bases:
            prefix = getattr(base, 'endpoint_prefix', None)
            if not prefix:
                continue
            prefixes.append(prefix)
        cls.endpoint_prefix = ''.join(prefixes)


class Resource(View, metaclass=MetaResource):
    # all available methods
    methods = HTTP_METHODS

    # the endpoint of the resource,
    # if this attr is None then this resource
    # will never be registered to the api
    endpoint = None

    # for toggling resource authentication
    auth_required = False

    auth_handler_class = None

    # a dict contains the method handlers of this resource
    method_handlers = {}

    endpoint_prefix = None

    def dispatch_request(self, *args, **kwargs):
        """The main flow of an api resource"""

        # check method available
        method_handler_class = self.method_handlers.get(request.method.upper())
        if not method_handler_class:
            raise HTTPError(error='MethodNotAllow',
                            status_code=405)

        # check authentication
        accessor = None
        if self.auth_handler_class:
            authentication_handler = self.auth_handler_class(
                secret_key=app.config['SECRET_KEY'],
                request=request
            )

            accessor = authentication_handler.run()
            if not accessor and self.auth_required:
                raise HTTPError(
                    error='Unauthorized',
                    status_code=401
                )

        # handle method
        method_handler = method_handler_class(
            accessor=accessor,
            request=request,
            app=app,
            redis=g.redis,
        )
        result = method_handler.run()

        if method_handler.redirect:
            return redirect(result)

        if method_handler.send_file:
            return send_file(result)

        return make_response(json.dumps(result, cls=CustomJsonEncoder),
                             200)


__all__ = (
    'Resource'
)
