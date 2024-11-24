from django.contrib import admin

from apps.webapp.models.post import Post


# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'summary']
    list_display_links = ['id', 'summary']


admin.site.register(Post, PostAdmin)
