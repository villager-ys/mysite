from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator


# Create your views here.
def blog_list(request):
    page_num = request.GET.get('page', 1)
    blogs = Blog.objects.all()
    ptr = Paginator(blogs, 10)
    blogs_with_page = ptr.get_page(page_num)
    content = {'blogs': blogs_with_page, 'blog_types': BlogType.objects.all()}
    return render_to_response('blog_list.html', content)


def blog_detail(request, blog_id):
    content = {'blog': get_object_or_404(Blog, id=blog_id)}
    return render_to_response('blog_detail.html', content)


def blog_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    content = {'blogs': Blog.objects.filter(blog_type=blog_type), 'blog_type': blog_type,
               'blog_types': BlogType.objects.all()}
    return render_to_response('blog_with_type.html', content)
