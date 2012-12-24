from django.db import models

class TestGae(models.Model):
    name = models.CharField(max_length=255)
    # Allow Extra because key name is included in path for blobinfo file store
    upload = models.FileField(upload_to='uploads', max_length=255)

    def __unicode__(self):
        return u'%s' % self.name
