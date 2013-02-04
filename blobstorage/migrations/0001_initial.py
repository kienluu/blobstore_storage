# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table('blobstorage_category', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
        ))
        db.send_create_signal('blobstorage', ['Category'])

        # Adding model 'File'
        db.create_table('blobstorage_file', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=255)),
        ))
        db.send_create_signal('blobstorage', ['File'])

        # Adding M2M table for field categories on 'File'
        db.create_table('blobstorage_file_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('file', models.ForeignKey(orm['blobstorage.file'], null=False)),
            ('category', models.ForeignKey(orm['blobstorage.category'], null=False))
        ))
        db.create_unique('blobstorage_file_categories', ['file_id', 'category_id'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table('blobstorage_category')

        # Deleting model 'File'
        db.delete_table('blobstorage_file')

        # Removing M2M table for field categories on 'File'
        db.delete_table('blobstorage_file_categories')


    models = {
        'blobstorage.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'})
        },
        'blobstorage.file': {
            'Meta': {'object_name': 'File'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blobstorage.Category']", 'symmetrical': 'False'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['blobstorage']