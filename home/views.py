from django.shortcuts import render ,get_object_or_404
from django.db.models import Q
from account.models import *
from django.http import HttpResponseRedirect,JsonResponse
from account.views import *

# Create your views here.
def home(request):
    return render(request,'home-page.html')


def blog_category(request):

    # Get all posts
    sports_posts = BlogsPost.objects.filter(category__category_name='SPORTS').order_by('created_at')
    news_posts = BlogsPost.objects.filter(category__category_name='NEWS').order_by('created_at')
    fashion_posts = BlogsPost.objects.filter(category__category_name='FASHION').order_by('created_at')

    # Get the active category pill from the query string
    active_pill = request.GET.get('category', 'news')

    # Pass data to template
    data = {
        'active_pill': active_pill,
        'sports_posts': sports_posts,
        'news_posts': news_posts,
        'fashion_posts': fashion_posts,
    }

    return render(request, 'blog-category.html', data)


def post_detail(request, post_id):
    detail = get_object_or_404(BlogsPost, pk=post_id)
    comments = detail.comment_set.all().order_by('-created_at')
    context = {
        'detail': detail,
        'comments': comments,
    }
    return render(request,'post_detail.html', context)

@login_required
def add_comment(request, post_id):
    """
    Process AJAX requests to add a comment.
    Expect a POST parameter 'comment' containing the comment text.
    """
    if request.method == "POST":
        post = get_object_or_404(BlogsPost, id=post_id)
        comment_text = request.POST.get('comment')
        if comment_text:
            # Use 'blog=post' and 'comment=comment_text' here
            comment = Comment.objects.create(user=request.user, blog=post, comment=comment_text)
            return JsonResponse({
                'username': request.user.username,
                'comment': comment.comment,  # Note: use comment.comment since the field is 'comment'
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)


# ~~~~~~~~~~~~~~~~~~~~~~~~Search filter~~~~~~~~~~~~~~~~~~~~
def search(request):
    if request.method == 'GET':
        query = request.GET.get('search','')
        
        search_username = User.objects.filter(username = query)
    #     blog_posts = BlogsPost.objects.filter(
    # Q(user__username__icontains=query) | Q(blog_title__icontains=query))
        blog_posts = BlogsPost.objects.filter(blog_title__icontains=query)
        data = {
                'blog_posts':blog_posts,
                'search_username':search_username}
        print(blog_posts)
        return render(request, 'search.html',data)
    
def profile_detail(request, username):
   user = get_object_or_404(User, username=username)
   print(user)
   queryset = BlogsPost.objects.filter(user = user)
   datas = {
       'user': user,
       'queryset': queryset
   }
   return render(request, "profile_detail.html", datas)
