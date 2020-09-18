from django.shortcuts import render,redirect
from .models import Article, Comment
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.
def article_list(request):
    articles=Article.objects.all().order_by('date')
    return render(request,'articles/article_list.html',{'articles':articles})

def article_details(request, slug):
    #return HttpResponse(slug)
    article=Article.objects.get(slug=slug)
    comments = article.comments.filter(active=False)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = forms.CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = article
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = forms.CommentForm()

    return render(request, 'articles/article_detail.html', {'article': article,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
    #return render(request,'articles/article_detail.html',{'article':article})

@login_required(login_url="/accounts/login/")
def article_create(request):
    form=forms.CreateArticle()
    if request.method=='POST':
        form=forms.CreateArticle(request.POST,request.FILES)
        if form.is_valid():
            #save article to database
            instance=form.save(commit=False)
            instance.author=request.user
            instance.save()
            return redirect('articles:list')
    else:
        return render(request,'articles/article_create.html',{'form':form})
