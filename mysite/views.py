from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.contrib import auth
from read_statistics.utils import get_seven_days_read_data, get_today_hot, get_yesterday_hot, get_7_days_hot
from blog.models import Blog


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates = cache.get('seven_days_read_data_dates')
    read_nums = cache.get('seven_days_read_data_read_nums')
    if dates is None or read_nums is None:
        dates, read_nums = get_seven_days_read_data(blog_content_type)
        cache.set_many({'seven_days_read_data_dates': dates, 'seven_days_read_data_read_nums': read_nums}, 3600)
    today_hot = get_today_hot(blog_content_type)
    yesterday_hot = get_yesterday_hot(blog_content_type)
    hot_for_7 = cache.get('hot_for_7')
    if hot_for_7 is None:
        hot_for_7 = get_7_days_hot()
        cache.set('hot_for_7', hot_for_7, 3600)
    context = {'dates': dates, 'read_nums': read_nums, 'today_hot': today_hot,
               'yesterday_hot': yesterday_hot, 'hot_for_7': hot_for_7}
    return render(request, 'home.html', context)


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username, password=password)
    if user is None:
        return render(request, 'error.html', {'message': '用户名或密码错误!!!'})
    else:
        auth.login(request, user)
        return redirect('/')
