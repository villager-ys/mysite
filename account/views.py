from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import LoginForm, RegisterForm


# Create your views here.
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


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    return render(request, 'user_info.html', {})
