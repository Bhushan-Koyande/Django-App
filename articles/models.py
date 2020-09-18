from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    title=models.CharField(max_length=100)
    slug=models.SlugField()
    body=models.TextField()
    date=models.DateTimeField(auto_now_add=True)
    thumb=models.ImageField(default='default.png',blank=True)
    author=models.ForeignKey(User,on_delete=models.DO_NOTHING,default=None)

    def __str__(self):
        return self.title

    def snippet(self):
        return self.body[:50]+"..."


class Comment(models.Model):
    post = models.ForeignKey(Article,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


#python manage.py makemigrations
#python manage.py migrate
