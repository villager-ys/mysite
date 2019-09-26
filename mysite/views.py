from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm, RegisterForm
from read_statistics.utils import get_seven_days_read_data, get_today_hot, \
    get_yesterday_hot, get_7_days_hot
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
    # get方法,请求登录页面,post方法,获取表单内容登录
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from'), reverse('home'))
    else:
        login_form = LoginForm()
    context = {'login_form': login_form}
    return render(request, 'login.html', context)


def register(request):
    # get方法,请求注册页面,post方法,获取表单内容注册
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 创建用户
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            email = register_form.cleaned_data['email']
            user = User.objects.create_user(username, email, password)
            user.save()
            # 跳转到登录页面
            return redirect(reverse('login'))
    else:
        register_form = RegisterForm()
    context = {'register_form': register_form}
    return render(request, 'register.html', context)
