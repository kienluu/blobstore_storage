# Django GAE Blobstore Storage
===

A django storage backend for google app engine blobstore.

## Usage
===

To make this the default storage place this in your setting.py file:

```python
DEFAULT_FILE_STORAGE = blobstore_storage.storage.BlobStoreStorage
```

One way to serve the files is you can include the urls.py from this app.  For example, 
place something similar to this in your app's url.py:

```python

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/', include('blobstore_storage.urls')),
)

```
