from django.shortcuts import render, get_object_or_404
from .models import Post
from .forms import CommentForm
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
# Create your views here.


def blogHome(request):
    object_list = Post.objects.filter(status=1).order_by('-created_on')
    feature_list = Post.objects.filter(featured=1).order_by('-created_on')

    paginator = Paginator(object_list, 4)
    top_list = feature_list[:3]
    page = request.GET.get('page')

    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an interger deliver the first page
        post_list = paginator.page(1)
    except EmptyPage:
        # if page is out of range, deliver last page of results
        post_list = paginator.page(paginator.num_pages)

    return render(request,
                  'blogapplication/index.html',
                  {'page': page,
                   'post_list': post_list,
                   'top_list': top_list},
                  )


def postDetail(request, slug):
    template_name = "blogapplication/post_detail.html"
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # create comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # assign the current post to the comment
            new_comment.post = post
            # save the comment to the database
            new_comment.save()

    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
