from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import Comments


def comment(request):
    refer = request.META.get('HTTP_REFERER', reverse('home'))
    object_id = int(request.POST.get('object_id', ''))
    content_type = request.POST.get('content-type', '')
    content = request.POST.get('comment', '').strip()
    user = request.user
    # 利用ContentType反向获取Blog对象
    model_class = ContentType.objects.get(model=content_type).model_class()
    obj_model = model_class.objects.get(id=object_id)
    comments = Comments()
    comments.user = user
    comments.content = content
    comments.content_object = obj_model
    comments.save()
    return redirect(refer)

