from django.conf.urls.defaults import *

from .views import BlobStoreFileServeView, BlobStoreImageServeView


urlpatterns = patterns('',
   url(r'^custom/serve/(?P<key>[ \w\.\/\-_]+\.(?P<ext>jpg|jpeg|png))/?$',
       BlobStoreImageServeView.as_view(), name='blobstore_image_serve'),
   url(r'^serve/(?P<key>[ \w\.\/\-_]+)/?$',
       BlobStoreFileServeView.as_view(), name='blobstore_serve'),
)

