from django.conf.urls.defaults import *

from .views import BlobStoreFileServeView, BlobStoreImageServeView


urlpatterns = patterns('',
   # The reverse() function will not work with the ((?P<size>[\d]+)/)? part below
   # so the resize value here is mandatory
   #url(r'^blobserve/resize/((?P<size>[\d]+)/)?/(?P<key>[ \w\.\/\-_]+\.(?P<ext>jpg|jpeg|png|gif))/?$',
   url(r'^blobserve/resize/(?P<size>[\d]+)/(?P<key>[ \w\.\/\-_]+\.(?P<ext>jpg|jpeg|png|gif))/?$',
       BlobStoreImageServeView.as_view(), name='blobstore_image_serve'),
   url(r'^blobserve/(?P<key>[ \w\.\/\-_]+)/?$',
       BlobStoreFileServeView.as_view(), name='blobstore_serve'),
)

