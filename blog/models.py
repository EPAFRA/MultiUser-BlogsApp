from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Posts(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
from django.db import models

class AboutPage(models.Model):
    title = models.CharField(max_length=100)
    introduction = models.TextField()
    story = models.TextField()
    team_member_1_name = models.CharField(max_length=100)
    team_member_1_title = models.CharField(max_length=100)
    team_member_1_image = models.ImageField(upload_to='team_images/')
    team_member_2_name = models.CharField(max_length=100)
    team_member_2_title = models.CharField(max_length=100)
    team_member_2_image = models.ImageField(upload_to='team_images/')
    team_member_3_name = models.CharField(max_length=100)
    team_member_3_title = models.CharField(max_length=100)
    team_member_3_image = models.ImageField(upload_to='team_images/')
    features = models.TextField()
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
    name = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    image = models.ImageField(upload_to='event_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title