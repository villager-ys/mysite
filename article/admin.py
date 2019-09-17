from django.contrib import admin
from .models import Article


# Register your models here.
# admin.site.register(Article)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'context', 'created_time', 'update_time', 'author', 'is_delete')
