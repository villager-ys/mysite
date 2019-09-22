from django.db import models
from django.contrib.auth.admin import User
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

    def blog_count(self):
        return self.blog_set.count()


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=30)
    context = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=False)
    is_delete = models.BooleanField(default=False)
    blog_type = models.ForeignKey(BlogType, on_delete=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '<Blog: %s>' % self.title

    class Meta:
        ordering = ['-create_time']
