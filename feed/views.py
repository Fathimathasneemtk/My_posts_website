from django.views.generic import ListView,DetailView,TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from follower.models import Follower
from .models import Post

class HomePage(TemplateView):
    http_method_names = ["get"]
    template_name='feed/home.html'
    
    def dispatch(self,request,*args,**kwargs):
        self.request=request
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            #values_list('following') without flat=True would return a list of tuples with one element each, like [(follower_id,), (follower_id,), ...].
            #values_list('following', flat=True) returns a flat list of follower IDs, like [follower_id, follower_id, ...].
            follower=list(Follower.objects.filter(followed_by=self.request.user).values_list('following',flat=True))
            #So, follower is a list containing the IDs of users who are followers of self.request.user.
            if follower:
                posts=Post.objects.filter(author__in=follower).order_by('-id')[0:30]
                #This line retrieves posts whose authors have IDs that match any ID in the follower_ids list, and the result is ordered by the id field in descending order, limited to the first 30 posts.
            else:
               posts=Post.objects.all().order_by('-id')[0:30] 
                
        else:
            posts=Post.objects.all().order_by('-id')[0:30]
        context["posts"] = posts
        return context

        
        

    
class PostDetailView(DetailView):
    http_methods=['get']
    template_name='feed/detail.html'
    context_object_name='post'
    model=Post
    
class PostCreateView(CreateView,LoginRequiredMixin):
    template_name='feed/new-post.html'
    model=Post
    fields=['text']
    success_url='/'
    
    def dispatch(self,request,*args,**kwargs):
        self.request=request
        return super().dispatch(request,*args,**kwargs)
    
    def form_valid(self, form):
        objects=form.save(commit=False)
        objects.author=self.request.user
        objects.save()
        return super().form_valid(form)
    
    def post(self,request,*args,**kwargs):
        post=Post.objects.create(
            text=request.POST.get("text"),
            author=request.user,
        )
        return render(
            request,
            "includes/post.html",
            {"post":post,
             "show_detail_view":True,},
            content_type="application/html"
        )
    
    
    
    
    

# Create your views here.
