from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary.models import CloudinaryField

class Posts(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    post_image = CloudinaryField('image', blank=True, null=True)  # Use CloudinaryField for images
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
from django.db import models

class AboutusPage(models.Model):
    title = models.CharField(max_length=100)
    who_are_we = models.TextField()
    what_we_do = models.TextField()
    mission = models.TextField()
    vission = models.TextField()
    join_us = models.TextField()
    contact_info = models.TextField()

    def __str__(self):
        return self.title
    
class Announcements(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    
class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comments')
    # name = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(default=timezone.now)
    event_image = CloudinaryField('image', blank=True, null=True)  # Use CloudinaryField for images
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title