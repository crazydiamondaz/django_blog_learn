from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.

class ArticleColumn(models.Model):
    title = models.CharField(max_length=100,blank=True)
    created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
class ArticlePost(models.Model):
    column = models.ForeignKey(
        ArticleColumn,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='article'
    )
    tags = TaggableManager(blank=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail',args=[self.id])

