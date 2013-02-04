# Create your views here.
import mimetypes
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.utils.encoding import smart_str
from django.views.generic import View
from .storage import BlobStoreStorage
from google.appengine.api.images import NotImageError, get_serving_url
import os


class BlobStoreFileServeView(View):

    _boolean_yes_states = ['1', 'yes', 'true', 'on']

    def get(self, request, *args, **kwargs):
        key = kwargs['key']
        storage = BlobStoreStorage()
        if storage.exists(key):
            mimetype, encoding = mimetypes.guess_type(kwargs['key']) or\
                                 ("application/x-octet-stream", None)
            response = HttpResponse(
                FileWrapper(storage.open(key)), mimetype=mimetype)
            if request.GET.get('download') in self._boolean_yes_states:
                response['Content-Disposition'] = smart_str(
                        u'attachment; filename=%s' % os.path.basename(key))
        else:
            response = HttpResponseNotFound()
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
            return HttpResponseRedirect(
                get_serving_url(storage._get_blobinfo(key), size=size))
        except NotImageError:
            return HttpResponseNotFound()

        """
        Size Available:

        IMG_SERVING_SIZES_LIMIT = 1600

        IMG_SERVING_SIZES = [
            32, 48, 64, 72, 80, 90, 94, 104, 110, 120, 128, 144,
            150, 160, 200, 220, 288, 320, 400, 512, 576, 640, 720,
            800, 912, 1024, 1152, 1280, 1440, 1600]

        Any size under 1600 seems to work?
        """