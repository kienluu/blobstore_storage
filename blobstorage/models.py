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
        index = self.file.name.find('/')
        if index > -1:
            return self.file.name[index + 1:]
        return self.file.name