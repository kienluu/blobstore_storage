import mimetypes
from django.conf import settings
from django.core.files import File
from django.core.files.storage import Storage
from django.core.urlresolvers import reverse
from google.appengine.api import files
from django.utils.encoding import force_unicode
from google.appengine.api.images import get_serving_url, NotImageError
from google.appengine.ext.blobstore import BlobInfo, BlobKey, delete,\
    BlobReader


class BlobStoreStorage(Storage):

    def __init__(self, location=None, base_url=None):
        if base_url is None:
            base_url = settings.MEDIA_URL
        self.base_url = base_url

    def _open(self, name, mode='rb'):
        return BlobStoreFile(name, mode, self)

    def path(self, name):
        name = name.strip()
        if name.startswith('./'):
            name = name[2:]
        return name

    def _save(self, name, content):
        name = name.replace('\\', '/')

        guessed_type = mimetypes.guess_type(name)[0]
        file_name = files.blobstore.create(
            mime_type=guessed_type or 'application/octet-stream',
            _blobinfo_uploaded_filename=name)

        with files.open(file_name, 'a') as f:
            for chunk in content.chunks(1024 * 128):
                f.write(chunk)

        files.finalize(file_name)

        data = files.blobstore.get_blob_key(file_name)

        if isinstance(data, (BlobInfo, BlobKey)):
            # We change the file name to the BlobKey's str() value.
            if isinstance(data, BlobInfo):
                data = data.key()
            return '%s/%s' % (data, name.lstrip('/'))
        else:
            raise ValueError("The App Engine Blobstore only supports "
                             "BlobInfo values. Data can't be uploaded "
                             "directly. You have to use the file upload "
                             "handler.")

    def delete(self, name):
        delete(self._get_key(name))

    def exists(self, name):
        return self._get_blobinfo(name) is not None

    def size(self, name):
        return self._get_blobinfo(name).size

    def url(self, name):
        return reverse('blobstore_serve', kwargs={'key': name})
#        try:
#            return get_serving_url(self._get_blobinfo(name))
#        except NotImageError:
#            return None

    def created_time(self, name):
        return self._get_blobinfo(name).creation

    def get_valid_name(self, name):
        return force_unicode(name).strip().replace('\\', '/')

    def get_available_name(self, name):
        return name.replace('\\', '/')

    def _get_key(self, name):
        return BlobKey(name.split('/', 1)[0])

    def _get_blobinfo(self, name):
        return BlobInfo.get(self._get_key(name))


class BlobStoreFile(File):
    def __init__(self, name, mode, storage):
        self.name = name
        self._storage = storage
        self._mode = mode
        self.blobstore_info = storage._get_blobinfo(name)

    @property
    def size(self):
        return self.blobstore_info.size

    def write(self, content):
        raise NotImplementedError()

    @property
    def file(self):
        if not hasattr(self, '_file'):
            self._file = BlobReader(self.blobstore_info.key())
        return self._file