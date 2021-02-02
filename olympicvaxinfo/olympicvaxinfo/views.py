from django.shortcuts import render
from olympicvaxinfo.models import Post, Comment, Category
from .forms import CommentForm

def get_latest_from_category(category):
    try:
        firstpost = Post.objects.filter(
            categories__name__contains=category.name
        ).order_by(
            '-created_on'
        )[0]
    except:
        firstpost = None
    return (firstpost)

def blog_index(request):
    posts = Post.objects.all().order_by('-created_on')
    categories = Category.objects.all().order_by('-name')
    categories_latests = []
    for c in categories:
        categories_latests.append(get_latest_from_category(c))
    context = {
        "posts": posts,
        "categories": categories,
        "categories_latests": categories_latests,
    }
    return render(request, "blog_index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(
        categories__name__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": category,
        "posts": posts
    }
    return render(request, "blog_category.html", context)

def blog_detail(request, pk):
    post = Post.objects.get(pk=pk)

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "blog_detail.html", context)