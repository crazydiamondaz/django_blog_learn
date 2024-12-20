from django.shortcuts import render
from django.http import HttpResponse
from .models import ArticlePost
# Create your views here.
def article_list(request):
    articles = ArticlePost.objects.all()
    context = {'articles':articles}
    return render(request,'article/list.html',context)

