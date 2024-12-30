from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ArticlePost
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import markdown
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.
def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        if order == 'total_views':
            # Use Q object to do joint research
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            ).order_by('-total_views')
        else:
            article_list = ArticlePost.objects.filter(
                Q(title__icontains=search) |
                Q(body__icontains=search)
            )
    else:
        search = ''
        if order == 'total_views':
            article_list = ArticlePost.objects.all().order_by('-total_views')
        else:
            article_list = ArticlePost.objects.all()
    # if request.GET.get('order') == 'total_views':
    #     article_list = ArticlePost.objects.all().order_by('-total_views')
    #     order = 'total_views'
    # else:
    #     article_list = ArticlePost.objects.all()
    #     order = 'normal'
    paginator = Paginator(article_list,6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {'articles': articles,'order': order,'search':search}
    return render(request,'article/list.html',context)

def article_detail(request,id):
    article = ArticlePost.objects.get(id=id)
    article.total_views += 1
    article.save(update_fields=['total_views'])
    article.body = markdown.markdown(article.body,
                                     extensions=['markdown.extensions.extra',
                                                 'markdown.extensions.codehilite',])
    context = {'article' : article}
    return render(request,'article/detail.html',context)

@login_required(login_url='/userprofile/login/')
def article_create(request):
    # if User Submit article
    if request.method == "POST":
        # store the data into Form Entity
        article_post_form = ArticlePostForm(data=request.POST)
        # Check the legality of the data
        if article_post_form.is_valid():
            # save the data and don't save it to the database
            new_article = article_post_form.save(commit=False)
            # point the id=1 User as the Author
            new_article.author = User.objects.get(id=request.user.id)
            # save the article to the dataset
            new_article.save()
            return redirect("article:article_list")
        # if the data is illegal, return error information
        else:
            return HttpResponse("Wrong content. Please refill the form.")
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)


@login_required(login_url='/userprofile/login/')
def article_delete(request,id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("Sorry, you can't delete this article.")
    article.delete()
    return redirect("article:article_list")
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request,id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("Sorry, you can't delete this article.")
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("Use POST Method please.")

@login_required(login_url='/userprofile/login/')
def article_update(request,id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("Sorry, you can't edit this article.")
    if request.method == "POST":
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            return redirect("article:article_detail",id=id)
        else:
            return HttpResponse("Wrong content. Please refill the form.")
    else:
        article_post_form = ArticlePostForm()
        context = {'article':article, 'article_post_form':article_post_form}
        return render(request,'article/update.html',context)




