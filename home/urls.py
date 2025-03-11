from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('',home,name='home'),
    path('blog_category/', blog_category,name='blog_category'),
    path('blog-category/<post_id>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/add-comment/', add_comment, name='add_comment'),
    path('search/',search,name = 'search'),
    path('profile-detail/<str:username>/',profile_detail,name = 'profile_detail'),
    
]
