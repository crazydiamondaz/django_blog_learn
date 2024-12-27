from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ArticlePost
from .forms import ArticlePostForm
from django.contrib.auth.models import User
import markdown
# Create your views here.
def article_list(request):
    articles = ArticlePost.objects.all()
    context = {'articles':articles}
    return render(request,'article/list.html',context)

def article_detail(request,id):
    article = ArticlePost.objects.get(id=id)
    article.body = markdown.markdown(article.body,
                                     extensions=['markdown.extensions.extra',
                                                 'markdown.extensions.codehilite',])
    context = {'article' : article}
    return render(request,'article/detail.html',context)

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
            new_article.author = User.objects.get(username='crazydiamond')
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

def article_delete(request,id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")

def article_safe_delete(request,id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("Use POST Method please.")

def article_update(request,id):
    article = ArticlePost.objects.get(id=id)
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




