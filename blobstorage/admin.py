from django.contrib import admin
from django.core.urlresolvers import reverse
import os
from blobstore_storage.blobstorage.models import Category, File



IMAGE_EXT_TYPES = ('.jpg', '.jpeg', '.gif', '.png')


class FileAdmin(admin.ModelAdmin):
    filter_horizontal = ['categories']
    list_display = ['__unicode__', 'thumbnail', 'copy_button']
    list_filter = ['categories']

    def thumbnail(self, file_instance):
        if os.path.splitext(file_instance.file.name)[1] in IMAGE_EXT_TYPES:
            url = reverse(
                'blobstore_image_serve',
                kwargs={'key': file_instance.file.name, 'size': '128'})
            return '<img src="%s"/>' % url
        return 'n/a'
    thumbnail.allow_tags = True

    def copy_button(self, file_instance):
        url = reverse(
            'blobstore_serve', kwargs={'key': file_instance.file.name})
        return '<a href="javascript:;" class="copy-to-clipboard-button" data-clipboard-text="%s" title="copy url to clipboard">Copy Link</a>' \
            % url
    copy_button.allow_tags = True

#    return '<button class="copy-file-url-button" '\
#           'data-clipboard-text="%s" '\
#           'title="copy url to clipboard">copy me</button>'\
#           % url



admin.site.register(Category)
admin.site.register(File, FileAdmin)