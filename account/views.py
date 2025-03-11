from django.shortcuts import render , get_object_or_404, redirect
from django.contrib.auth import authenticate , login ,logout
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,JsonResponse
from .models import *
from django.core.mail import send_mail,EmailMessage
from django.conf import settings


# Create your views here.
def user_blog_creation(request):
    return render(request,'blog_creation_page.html')

def contact(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            content = request.POST.get('content')
        
            subject = f"Submission from Contact form by{name}"
            message = f"Name: {name}\n\nEmail: {email}\n\nMessage:{content}"
            send_mail(
            subject,message,email,['iamkhan6056@gmail.com'],fail_silently=False
            )
        return redirect('success')
    except:
        message.error(request,"Some unexpected error!")
    return render(request,'contact.html')
def success(request):
    return render(request,'success.html')

@login_required
def start_bloging(request):
    return render(request,'post_admin.html')  

@login_required 
def post_admin(request):
    try:
      user_posts = BlogsPost.objects.filter(user = request.user)
    except:
        messages.error(request,"Some thing went wrong.")
    
    return render(request,'post_admin.html',{'user_posts':user_posts})    

# ```````````````````````````ADD POSTS```````````````````````````````
@login_required
def create_post(request):
    try:
        categories = Category.objects.all()
        if request.method == 'POST':
            title = request.POST.get('title')
            contant = request.POST.get('contant')
            image = request.FILES.get('thumbnil')
            category_id = request.POST.get('category')
            category = Category.objects.get(id=category_id)
            BlogsPost.objects.create(
                user = request.user,
                blog_title =  title,
                blog_content = contant,
                blog_images = image,
                category = category )
            messages.success(request,"Blog posted successfully..")
            return redirect('post_admin')
    except:
        messages.error(request,"Blog posting failed..")
        
        
    return render(request,'create_post.html',{'categories':categories})    


# ``````````````````````LOGIN``````````````````````````````````
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, email = email, password = password)
        if user is not None:
            login(request,user)
            messages.success(request, 'Successfully login...')
            return redirect('post_admin')
        else:
            messages.error(request, 'Invalid username or password')
            return HttpResponseRedirect(reverse('login'))
    return render(request,'login.html')


# ``````````````````````REGISTERATION``````````````````````````
def user_registeration(request):
    if request.method == 'POST':
        data = request.POST
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        profile_image = request.FILES.get('image')
        
        
        if not username or not email or not password:
            messages.error(request, 'All fields are required')
            return redirect('sign_up')
        
        if password !=confirm_password:
            messages.error(request,'Enter same passwad')
            return redirect('sign_up')
        if User.objects.filter(email=email).exists():
            messages.error(request,'Email already exists')
            return redirect('sign_up')

        user = User(email=email, username=username, profile_image=profile_image)
        user.set_password(password)
        user.save()
        messages.success(request,'User created successfully')
        return redirect('login')
    return render(request,'register.html')
# ``````````````````````````````````````LOGOUT``````````````````````
def log_out(request):
    logout(request)
    messages.success(request,'Loged out successfully')
    return redirect('home')


# ``````````````````user forget passward otp by email``````````````````````````
def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)

            new_password_reset = ResetPasswordToken(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')

    return render(request,'forgotpassward.html')

def PasswordResetSent(request, reset_id):

    if ResetPasswordToken.objects.filter(reset_id=reset_id).exists():
        return render(request, 'passward_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')
    
def ResetPassword(request, reset_id):

    try:
        password_reset_id = ResetPasswordToken.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            expiration_time = password_reset_id.created_at + timezone.timedelta(minutes=5)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()
                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')
            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)

    
    except ResetPasswordToken.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'reset_password.html')   

# `````````````````````````POST EDITIONS`````````````````````````````
@login_required
def edit_post(request, post_id):
    try:
     categories = Category.objects.all()
     post_instance = get_object_or_404(BlogsPost, pk=post_id, user= request.user)
     if request.method == 'POST':
        title = request.POST.get('title')
        contant = request.POST.get('contant')
        image = request.FILES.get('thumbnil')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        if title and contant and image and category:
            post_instance.blog_title = title
            post_instance.blog_content = contant
            post_instance.blog_images = image
            post_instance.category = category
            post_instance.save()
            messages.success(request,"Post edited sucessfully...")
            return redirect('post_admin')
    except:
        messages.error(request,"Message was not edited sucessfully...")
            
    return render(request, 'update.html',{'post_instance':post_instance,'categories':categories})



# `````````````````````````POST DELETION`````````````````````````````
@login_required
def delete_post(request, post_id):
    # Check if the user is the author of the post
    post = get_object_or_404(BlogsPost, pk=post_id)
    if post.user != request.user:
        messages.success(request,"Unabel to delete this post..")
        return JsonResponse({'status': 'error', 'message': 'You are not the author of this post.'}, status=403)

    # Handle POST request for deletion
    if request.method == 'POST':
        # Perform deletion
        post.delete()
        messages.success(request, "Post deleted successfully")
        return redirect('post_admin')

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)


# `````````````````````````````````post_admin_detail`````````````````````
def post_admin_detail(request,post_id):
    detail  = get_object_or_404(BlogsPost,pk=post_id)
    comments = detail.comment_set.all().order_by('-created_at')
    context = {
        'detail': detail,  # using "detail" as in your template
        'comments': comments,
    }
    
    return render(request,'post_admin_detail.html',context)


# ```````````````````````````like dislike and comment`````````````````````````

@login_required
def like_dislike_post(request, post_id):
    """
    Process AJAX requests for liking or disliking a post.
    Expect a POST parameter 'like': '1' for like and '0' for dislike.
    """
    if request.method == "POST":
        blog = get_object_or_404(BlogsPost, id=post_id)
        like_value = request.POST.get('like')
        like_bool = True if like_value == '1' else False

        # Get or create the reaction record.
        reaction, created = LikeDislike.objects.get_or_create(user=request.user, blog=blog)

        if not created:
            # If the same reaction is clicked, remove it.
            if reaction.like == like_bool:
                reaction.delete()
            else:
                # Update the reaction.
                reaction.like = like_bool
                reaction.save()
        else:
            reaction.like = like_bool
            reaction.save()

        return JsonResponse({
            'likes': blog.total_likes(),
            'dislikes': blog.total_dislikes()
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def add_comment(request, post_id):
    """
    Process AJAX requests to add a comment.
    Expect a POST parameter 'comment' containing the comment text.
    """
    if request.method == "POST":
        post = get_object_or_404(BlogsPost, id=post_id)
        comment_text = request.POST.get('comment')
        print(comment_text)
        if comment_text:
            # Use 'blog=post' and 'comment=comment_text' here
            comment = Comment.objects.create(user=request.user, blog=post, comment=comment_text)
            comment.save()
            profile_image_url = request.user.profile_image.url if request.user.profile_image else "/static/img/defaultimage.png"
            print("comment saved")
            return JsonResponse({
                'username': request.user.username,
                'profile_image': profile_image_url,
                'comment': comment.comment,  # Note: use comment.comment since the field is 'comment'
                'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M')
            })
    print("comment not saved")        
    return JsonResponse({'error': 'Invalid request'}, status=400)
