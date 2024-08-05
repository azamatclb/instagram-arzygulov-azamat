from django.contrib import admin

from webapp.models import Post


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary']
    list_display_links = ['id', 'summary']


admin.site.register(Post, PostAdmin)
