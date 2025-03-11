from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import *
# Register your models here.
class UserAdmin(DefaultUserAdmin):
    list_display = ['username','email','password','profile_image']
    
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['user','get_username','blog_title','blog_images','category','created_at','updated_at']    
    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'
    
    
admin.site.register(User, UserAdmin)    
admin.site.register(BlogsPost, BlogPostAdmin)
admin.site.register(Category)
admin.site.register(ResetPasswordToken)
admin.site.register(LikeDislike)
admin.site.register(Comment)