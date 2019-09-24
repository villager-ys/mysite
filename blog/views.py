from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog, BlogType
from read_statistics.utils import read_statistics_once_read


# Create your views here.
def blog_list(request):
    page_num = request.GET.get('page', 1)
    blogs = Blog.objects.all()
    blogs_with_page, page_size, dates = get_page_content(blogs, page_num)
    date_dist = {}
    for date in dates:
        blog_count = Blog.objects.filter(create_time__year=date.year, create_time__month=date.month).count()
        date_dist[date] = blog_count
    content = {'blogs': blogs_with_page, 'blog_types': BlogType.objects.all(),
               'page_size': page_size, 'dates': date_dist}
    return render(request, 'blog_list.html', content)


def blog_detail(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    read_cookie_key = read_statistics_once_read(request, blog)
    previous_blog = Blog.objects.filter(create_time__gt=blog.create_time).last()
    next_blog = Blog.objects.filter(create_time__lt=blog.create_time).first()
    content = {'blog': blog, 'previous_blog': previous_blog, 'next_blog': next_blog}
    response = render(request, 'blog_detail.html', content)
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
    return response


def blog_with_type(request, blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs = Blog.objects.filter(blog_type=blog_type)
    page_num = request.GET.get('page', 1)
    blogs_with_page, page_size, dates = get_page_content(blogs, page_num)
    content = {'blogs': blogs_with_page, 'blog_type': blog_type,
               'blog_types': BlogType.objects.all(), 'page_size':
                   page_size, 'dates': dates}
    return render(request, 'blog_with_type.html', content)


def get_page_content(blogs, page_num):
    ptr = Paginator(blogs, settings.EACH_PAGE_BLOG_NUM)
    blogs_with_page = ptr.get_page(page_num)
    current_page_num = blogs_with_page.number  # 获取当前页码
    total = ptr.num_pages  # 获取最大页数
    page_size = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, total) + 1))
    # 加上省略号 # 不是第一页加上第一页,不是最后一个追加最后一页
    if page_size[0] - 1 >= 1:
        page_size.insert(0, 1)
        page_size.insert(1, '...')
    if total - page_size[-1] >= 1:
        page_size.append('...')
        page_size.append(total)
    dates = Blog.objects.dates('create_time', 'month', order='DESC')
    return blogs_with_page, page_size, dates


def blog_with_date(request, year, month):
    blogs = Blog.objects.filter(create_time__year=year, create_time__month=month)
    page_num = request.GET.get('page', 1)
    blogs_with_page, page_size, dates = get_page_content(blogs, page_num)
    current_date = '%s年%s月' % (year, month)
    content = {'blogs': blogs_with_page, 'blog_types': BlogType.objects.all(),
               'page_size': page_size, 'dates': dates, 'current_date': current_date}
    return render(request, 'blog_with_date.html', content)
