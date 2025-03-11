from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Please provide an email address.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField(max_length=150, unique=True)
    profile_image = models.ImageField(upload_to='profile_pictures', null=True, blank=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Only username is required, email is primary

    def __str__(self):
        return self.email
class Category(models.Model):
    options = [
        ('NEWS', 'NEWS'),
        ('FASHION', 'FASHION'),
        ('SPORTS', 'SPORTS'),
        
  ]
    category_name = models.CharField(max_length=20,choices=options, default='NEWS')
    def __str__(self):
         return self.category_name
    
class BlogsPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='user')
    blog_title = models.CharField(max_length=200)
    blog_content = models.TextField()
    blog_images = models.ImageField(upload_to='blog_pictures/',null=True, blank=True)   
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    created_at = models.DateTimeField(default=timezone.now)  # Automatically set to now
    updated_at = models.DateTimeField(auto_now=True)
    
    def total_likes(self):
        return self.likedislike_set.filter(like=True).count()

    def total_dislikes(self):
        return self.likedislike_set.filter(like=False).count()
    
# ````````````````Forgot password````````````````````    
class ResetPasswordToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reset_password_token')
    reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Passward reset for {self.user.username} at {self.created_at}."
    
    
class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_dislike_user')
    blog = models.ForeignKey(BlogsPost, on_delete=models.CASCADE)
    like = models.BooleanField(default=False ,null=True ,blank=True)
    
    def __str__(self):
        return f"{self.user.username} likes/dislikes {self.blog.blog_title}."
    
    class Meta:
        unique_together = ('user', 'blog')
        
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    blog = models.ForeignKey(BlogsPost, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"{self.user.username} commented on {self.blog.blog_title}."