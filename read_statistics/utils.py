import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum, F
from .models import ReadNum, ReadDetail
from blog.models import Blog


def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" % (ct.model, obj.pk)

    if not request.COOKIES.get(key):
        # 总阅读数 +1
        read_num, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # F() django内置表达式,好处：F()允许Django在未实际链接数据的情况下具有对数据库字段的值的引用，
        # 不用获取对象放在内存中再对字段进行操作，直接执行原生产sql语句操作
        read_num.read_num = F('read_num') + 1
        read_num.save()

        # 当天阅读数 +1
        date = timezone.now().date()
        read_detail, _ = ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        read_detail.read_num = F('read_num') + 1
        read_detail.save()
    return key


def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates = []
    read_nums = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        # 聚合查询
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return dates, read_nums


def get_today_hot(content_type):
    today = timezone.now().date()
    # QuerySet 的Limit,使用Python 的切片语法来限制 QuerySet 记录的数目。它等同于SQL 的LIMIT和 OFFSET 子句
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')[:7]
    return read_details


def get_yesterday_hot(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')[:7]
    return read_details


def get_7_days_hot():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    # 获取7天内的热门博客　
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date)\
                .values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num'))\
                .order_by('-read_num_sum')[:7]
    return blogs

