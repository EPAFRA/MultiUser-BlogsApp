from django.shortcuts import render, get_object_or_404,redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import Posts,Comment,AboutPage,Announcements,Event
from django.views.generic import ListView,DetailView,CreateView,DeleteView,UpdateView
from .forms import CommentForm,AnnouncementForm,EventForm

def home(request):
    context = {
        'posts': Posts.objects.all
    }
    return render(request, 'blog/home.html', context)

class PostListView(ListView):
    model = Posts
    template_name='blog/home.html' #<app>/<model>_<listtype>.html
    context_object_name = 'posts'
    ordering=['-date_posted']
    paginate_by=5

class UserPostListView(ListView):
    model = Posts
    template_name='blog/user_posts.html' #<app>/<model>_<listtype>.html
    context_object_name = 'posts'
    ordering=['-date_posted']
    paginate_by=5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date_posted')
        

class PostDetailView(DetailView):
    model = Posts

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post= self.get_object()
        if self.request.user == post.author:
            return True
        return False
        # return self.get_object().author == self.request.user

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Posts
    success_url = '/'

    def test_func(self):
        post= self.get_object()
        if self.request.user == post.author:
            return True
        return False
    
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Posts, id=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'  # Create this template to confirm deletion
    # success_url = reverse_lazy ('post-detail' object.post.pk)  # Redirect to home after deletion
    # success_url = '/'
    def get_success_url(self):
        # Redirect to the detail page of the post after deleting a comment
        return reverse_lazy('post-detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.post.author
    

def about(request):
    about_page = AboutPage.objects.first()
    return render(request, 'blog/about.html',{'about_page': about_page})

class LatestPostsView(ListView):
    model = Posts
    template_name = 'blog/latest_posts.html'  # Template to display latest posts
    context_object_name = 'latest_posts'
    ordering = ['-date_posted']
    paginate_by = 5 

class AnnouncementListView(ListView):
    model = Announcements
    template_name = 'blog/announcements.html'  # Template to display announcements
    context_object_name = 'announcements'
    ordering = ['-date_posted']  # Order announcements by date posted
    paginate_by = 5 


class AnnouncementDetailView(DetailView):
    model = Announcements
    template_name = 'blog/announcement_detail.html'

class AnnouncementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Announcements
    form_class = AnnouncementForm
    template_name = 'blog/announcement_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        # Only allow access if the user is an admin
        return self.request.user.is_staff

    def get_success_url(self):
        return reverse_lazy('announcements')

class AnnouncementDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Announcements
    success_url = '/'

    def test_func(self):
        post= self.get_object()
        if self.request.user == Announcements.author:
            return True
        return False
    
class AnnouncementDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Announcements
    template_name = 'blog/announcement_confirm_delete.html'
    success_url = reverse_lazy('announcements')  # Redirect to the announcements list after deletion

    def test_func(self):
        announcement = self.get_object()
        return self.request.user.is_staff
    
def calendar_view(request):
    events = Event.objects.all()  # Fetch events from the database
    context = {
        'events': events
    }
    return render(request, 'blog/calender.html', context)

class EventDetailView(DetailView):
    model = Event
    template_name = 'blog/event_detail.html'  # The template to render

    def get_object(self, queryset=None):
        """Override get_object to provide the event based on the primary key"""
        pk = self.kwargs.get('pk')
        return get_object_or_404(Event, pk=pk)
    
class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'blog/event_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the current user as the event author
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('event-detail', kwargs={'pk': self.object.pk})
    
class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'blog/event_form.html'

    def get_success_url(self):
        return reverse_lazy('event-detail', kwargs={'pk': self.object.pk})
    
class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'blog/event_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('calendar-view')
    
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # Send email (adjust email settings as needed)
            send_mail(
                subject=f'Contact form submission from {name}',
                message=message,
                from_email=email,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            
            # Redirect to a success page or display a success message
            return redirect('contact-success')
    else:
        form = ContactForm()
    
    return render(request, 'blog/contact.html', {'form': form})

def contact_success(request):
    return render(request, 'blog/contact_success.html')

# Create your views here.
