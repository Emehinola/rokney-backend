from django.contrib import admin
from . models import Comment, Post, Like, FileAlbum

# Register your models here.
admin.site.register(Comment)
admin.site.register(Like)


class PostAlbumAdmin(admin.StackedInline):
    model = FileAlbum


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    inlines = [PostAlbumAdmin]  # stacks the file album in the post edit page

    class Meta:
        model = Post


@admin.register(FileAlbum)
class PostAlbumAdmin(admin.ModelAdmin):
    pass
