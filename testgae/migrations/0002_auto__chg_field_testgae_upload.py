# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'TestGae.upload'
        db.alter_column('testgae_testgae', 'upload', self.gf('django.db.models.fields.files.FileField')(max_length=255))

    def backwards(self, orm):

        # Changing field 'TestGae.upload'
        db.alter_column('testgae_testgae', 'upload', self.gf('django.db.models.fields.files.FileField')(max_length=100))

    models = {
        'testgae.testgae': {
            'Meta': {'object_name': 'TestGae'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'upload': ('django.db.models.fields.files.FileField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['testgae']