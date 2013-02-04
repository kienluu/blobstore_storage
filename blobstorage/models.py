import logging
from django.db import models
from blobstore_storage.storage import BlobStoreStorage

class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return unicode(self.name)

class File(models.Model):
    file = models.FileField(
        storage=BlobStoreStorage(), upload_to='blobs/', max_length=255)
    categories = models.ManyToManyField(Category)

    def __unicode__(self):
        return self.file.name[65:]