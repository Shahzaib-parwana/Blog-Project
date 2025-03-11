from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('create-blog/',user_blog_creation,name='blog_creation'),# create blog wala page
    path('start-bloging/',start_bloging,name='start_bloging'),# create blog k ander button (start bloging)
    path('post_admin/',post_admin,name='post_admin'),
    path('create_post/',create_post,name='create_post'),
    path('contact-us/',contact,name='contact'),
    path('post-admin-detail/<post_id>/',post_admin_detail,name='post_admin_detail'),
    path('edit-post/<post_id>/',edit_post,name='edit_post'),
    path('post/<int:post_id>/delete/', delete_post, name='delete_post'),
    
   
    
    path('login-page/',user_login,name='login'),
    path('log-out/',log_out,name='log_out'),
    path('sign-up/',user_registeration,name='sign_up'),
    path('success/',success,name='success'),
    path('forgot-password/', ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', ResetPassword, name='reset-password'),
    path('post/<int:post_id>/like-dislike/', like_dislike_post, name='like_dislike_post'),
    path('post/<int:post_id>/add-comment/', add_comment, name='add_comment'),
]
