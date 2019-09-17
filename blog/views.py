from django.shortcuts import render, render_to_response, get_object_or_404
from .models import Blog, BlogType


# Create your views here.
def blog_list(request):
    content = {'blogs': Blog.objects.all()}
    return render_to_response('blog_list.html', content)


def blog_detail(request, blog_id):
    content = {'blog': get_object_or_404(Blog, id=blog_id)}
    return render_to_response('blog_detail.html', content)


def blog_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    content = {'blogs': Blog.objects.filter(blog_type=blog_type), 'blog_type': blog_type}
    return render_to_response('blog_with_type.html', content)
