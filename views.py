# Create your views here.
import mimetypes
from django.core.servers.basehttp import FileWrapper
from django import http
from django.utils.encoding import smart_str
# from django.views.generic import View
from .storage import BlobStoreStorage
from google.appengine.api.images import NotImageError, get_serving_url
import os

from django.utils.decorators import classonlymethod
from django.utils import six


import logging
from functools import update_wrapper

logger = logging.getLogger('django.request')


class View(object):
    """
    Intentionally simple parent class for all views. Only implements
    dispatch-by-method and simple sanity checking.
    """

    http_method_names = ['get', 'post', 'put', 'delete', 'head', 'options', 'trace']

    def __init__(self, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in six.iteritems(kwargs):
            setattr(self, key, value)

    @classonlymethod
    def as_view(cls, **initkwargs):
        """
        Main entry point for a request-response process.
        """
        # sanitize keyword arguments
        for key in initkwargs:
            if key in cls.http_method_names:
                raise TypeError("You tried to pass in the %s method name as a "
                                "keyword argument to %s(). Don't do that."
                                % (key, cls.__name__))
            if not hasattr(cls, key):
                raise TypeError("%s() received an invalid keyword %r. as_view "
                                "only accepts arguments that are already "
                                "attributes of the class." % (cls.__name__, key))

        def view(request, *args, **kwargs):
            self = cls(**initkwargs)
            if hasattr(self, 'get') and not hasattr(self, 'head'):
                self.head = self.get
            self.request = request
            self.args = args
            self.kwargs = kwargs
            return self.dispatch(request, *args, **kwargs)

        # take name and docstring from class
        update_wrapper(view, cls, updated=())

        # and possible attributes set by decorators
        # like csrf_exempt from dispatch
        update_wrapper(view, cls.dispatch, assigned=())
        return view

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def http_method_not_allowed(self, request, *args, **kwargs):
        logger.warning('Method Not Allowed (%s): %s', request.method, request.path,
            extra={
                'status_code': 405,
                'request': self.request
            }
        )
        return http.HttpResponseNotAllowed(self._allowed_methods())

    def options(self, request, *args, **kwargs):
        """
        Handles responding to requests for the OPTIONS HTTP verb.
        """
        response = http.HttpResponse()
        response['Allow'] = ', '.join(self._allowed_methods())
        response['Content-Length'] = '0'
        return response

    def _allowed_methods(self):
        return [m.upper() for m in self.http_method_names if hasattr(self, m)]

class BlobStoreFileServeView(View):

    _boolean_yes_states = ['1', 'yes', 'true', 'on']

    def get(self, request, *args, **kwargs):
        key = kwargs['key']
        storage = BlobStoreStorage()
        if storage.exists(key):
            mimetype, encoding = mimetypes.guess_type(kwargs['key']) or\
                                 ("application/x-octet-stream", None)
            response = http.HttpResponse(
                FileWrapper(storage.open(key)), mimetype=mimetype)
            if request.GET.get('download') in self._boolean_yes_states:
                response['Content-Disposition'] = smart_str(
                        u'attachment; filename=%s' % os.path.basename(key))
        else:
            response = http.HttpResponseNotFound()
        return response


class BlobStoreImageServeView(View):
    """
    Use this to serve resized images with app engines get_serving_url function.

    TODO: Find out where these images are stored and if they cost money to use.
    """

    def get(self, request, *args, **kwargs):
        key = kwargs['key']
        size = kwargs.get('size')
        if size:
            size = int(size)
        storage = BlobStoreStorage()
        try:
            # Default serving size is 512
            return http.HttpResponseRedirect(
                get_serving_url(storage._get_blobinfo(key), size=size))
        except NotImageError:
            return http.HttpResponseNotFound()

        """
        Size Available:

        IMG_SERVING_SIZES_LIMIT = 1600

        IMG_SERVING_SIZES = [
            32, 48, 64, 72, 80, 90, 94, 104, 110, 120, 128, 144,
            150, 160, 200, 220, 288, 320, 400, 512, 576, 640, 720,
            800, 912, 1024, 1152, 1280, 1440, 1600]

        Any size under 1600 seems to work?
        """