from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ArticlePost,ArticleColumn
from .forms import ArticlePostForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import markdown
from django.core.paginator import Paginator
from django.db.models import Q
from comment.models import Comment
# Create your views here.
def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    column = request.GET.get('column')
    tag = request.GET.get('tag')

    article_list = ArticlePost.objects.all()
    if search:
        article_list = article_list.filter(
            Q(title__icontains=search) |
            Q(body__icontains=search)
        )
    else:
        search = ''
    if column is not None and column.isdigit():
        article_list = article_list.filter(column=column)
    if tag and tag != 'None':
        article_list = article_list.filter(tags__name__in=[tag])
    if order == 'total_views':
        article_list = article_list.order_by('-total_views')
    #     if order == 'total_views':
    #         # Use Q object to do joint research
    #         article_list = ArticlePost.objects.filter(
    #             Q(title__icontains=search) |
    #             Q(body__icontains=search)
    #         ).order_by('-total_views')
    #     else:
    #         article_list = ArticlePost.objects.filter(
    #             Q(title__icontains=search) |
    #             Q(body__icontains=search)
    #         )
    # else:
    #     search = ''
    #     if order == 'total_views':
    #         article_list = ArticlePost.objects.all().order_by('-total_views')
    #     else:
    #         article_list = ArticlePost.objects.all()
    # if request.GET.get('order') == 'total_views':
    #     article_list = ArticlePost.objects.all().order_by('-total_views')
    #     order = 'total_views'
    # else:
    #     article_list = ArticlePost.objects.all()
    #     order = 'normal'
    paginator = Paginator(article_list,6)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    context = {'articles': articles,
               'order': order,
               'search':search,
               'column':column,
               'tag':tag,
               }
    return render(request,'article/list.html',context)

def article_detail(request,id):
    article = ArticlePost.objects.get(id=id)
    comments = Comment.objects.filter(article=id)
    article.total_views += 1
    article.save(update_fields=['total_views'])
    md = markdown.Markdown(extensions=['markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',])
    article.body = md.convert(article.body)
    context = {'article' : article, 'toc' : md.toc,'comments':comments}
    return render(request,'article/detail.html',context)

@login_required(login_url='/userprofile/login/')
def article_create(request):
    # if User Submit article
    if request.method == "POST":
        # store the data into Form Entity
        article_post_form = ArticlePostForm(request.POST,request.FILES)
        # Check the legality of the data
        if article_post_form.is_valid():
            # save the data and don't save it to the database
            new_article = article_post_form.save(commit=False)
            # point the id=1 User as the Author
            new_article.author = User.objects.get(id=request.user.id)
            # save the article to the dataset
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()
            article_post_form.save_m2m()
            return redirect("article:article_list")
        # if the data is illegal, return error information
        else:
            return HttpResponse("Wrong content. Please refill the form.")
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form,'columns':columns}
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
            if request.FILES.get('avatar'):
                article.avatar = request.FILES.get('avatar')
            # print(*request.POST.get('tags').split(','))
            # article.tags.set(*request.POST.get('tags').split(','), clear=True)
            article.title = request.POST['title']
            article.body = request.POST['body']
            if request.POST['column'] != 'none':
                article.column = ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column = None
            article.save()
            return redirect("article:article_detail",id=id)
        else:
            return HttpResponse("Wrong content. Please refill the form.")
    else:
        article_post_form = ArticlePostForm()
        columns = ArticleColumn.objects.all()
        context = {'article':article, 'article_post_form':article_post_form,'columns':columns,
                   'tags':','.join([x for x in article.tags.names()]),}
        return render(request,'article/update.html',context)




