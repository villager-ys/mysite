from django.shortcuts import render_to_response, get_object_or_404
from .models import Article


# Create your views here.
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    context = {'article': article}
    return render_to_response("article_detail.html", context)


def article_list(request):
    articles = Article.objects.filter(is_delete=False)
    context = {'articles': articles}
    return render_to_response('article_list.html', context)
