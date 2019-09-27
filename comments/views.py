from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Comments
from .forms import CommentsForm


@csrf_exempt
def comment(request):
    refer = request.META.get('HTTP_REFERER', reverse('home'))
    user = request.user
    data = {}
    comments_form = CommentsForm(request.POST, user=user)
    if comments_form.is_valid():
        comments = Comments()
        comments.object_id = comments_form.cleaned_data['object_id']
        comments.user = comments_form.cleaned_data['user']
        comments.content_object = comments_form.cleaned_data['model_obj']
        comments.content = comments_form.cleaned_data['comment']
        comments.save()
        # 返回数据
        data['status'] = 'SUCCESS'
        data['username'] = comments.user.username
        data['comment_time'] = comments.create_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text'] = comments.content
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comments_form.errors.values())[0][0]
    return JsonResponse(data)
