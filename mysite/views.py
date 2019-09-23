from django.shortcuts import render_to_response
from django.contrib.contenttypes.models import ContentType
from read_statistics.utils import get_seven_days_read_data, get_today_hot, get_yesterday_hot, get_7_days_hot
from blog.models import Blog


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    today_hot = get_today_hot(blog_content_type)
    yesterday_hot = get_yesterday_hot(blog_content_type)
    hot_for_7 = get_7_days_hot()
    context = {'dates': dates, 'read_nums': read_nums, 'today_hot': today_hot,
               'yesterday_hot': yesterday_hot, 'hot_for_7': hot_for_7}
    return render_to_response('home.html', context)
