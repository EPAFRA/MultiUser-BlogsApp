from django.urls import path
from. import views
from .views import PostListView,EventDetailView,EventCreateView,EventDeleteView,EventUpdateView,LatestPostsView,AnnouncementDeleteView,AnnouncementCreateView,AnnouncementListView,AnnouncementDetailView,PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,UserPostListView,CommentCreateView,CommentDeleteView,calendar_view



urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('latest-posts/', LatestPostsView.as_view(), name='latest-posts'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'), 
    path('posts/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
     path('announcements/', AnnouncementListView.as_view(), name='announcements'),
    path('announcements/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    path('announcements/create/', AnnouncementCreateView.as_view(), name='announcement-create'),
    path('announcement/<int:pk>/delete/', AnnouncementDeleteView.as_view(), name='announcement-delete'),
    path('calendar/', calendar_view, name='calendar-view'),
    path('event/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
     path('event/create/', EventCreateView.as_view(), name='event-create'),
    path('event/<int:pk>/edit/', EventUpdateView.as_view(), name='event-update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event-delete'),
      path('contact/', views.contact_view, name='contact'),
    path('contact-success/', views.contact_success, name='contact-success'),
    path('post/<int:pk>/like/', views.like_post, name='like-post'),
    
    path('about/', views.about, name='blog-about'),
    # path('contact/', views.contact, name='contact'),
]

