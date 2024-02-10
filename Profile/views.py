from django.views.generic import DetailView,UpdateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBadRequest,JsonResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import update_session_auth_hash
from feed.models import Post
from follower.models import Follower

class ProfileDetailView(DetailView):
    http_method_names=["get"]
    model = User
    context_object_name="user"
    template_name="profile/detail.html"
    slug_field="username"
    slug_url_kwarg = 'username'
    
    def dispatch(self,request,*args,**kwargs):
        self.request=request
        return super().dispatch(request,*args,**kwargs)
    
    
        
    
    def get_context_data(self,**kwargs) :
        user=self.get_object()
        context = super().get_context_data(**kwargs)
        context["total_posts"] = Post.objects.filter(author=user).count()
        context["total_followers"]=Follower.objects.filter(following=user).count()
        if self.request.user.is_authenticated:
            context["you_follow"]=Follower.objects.filter(followed_by=self.request.user,following=user).exists()
            return context
"""button click->action and user is send from js->in views---checking that sended user is exist,checking the s
sended data has action and user,checking the action if it is "follow"  check the follwwing object is already there unless create it.
--if action is "unfollow" ,checking that following object is there..if it is there delete that following user that is the unfollow.
--then send a jsonresponse from views.py into js saying it is sucess and wording i the button.
"""    
class FollowView(LoginRequiredMixin,View):
    http_method_names=["post"]
    def post(self,request,*args,**kwargs):
        data=request.POST.dict()
        if "action" not in data or "username" not in data:
            return HttpResponseBadRequest("Missing data")
        try:   
            other_user=User.objects.get(username=data["username"])
        except User.DeosNotExist:
            return HttpResponseBadRequest("Missing user")
        if data["action"]=="follow":
            follower,created=Follower.objects.get_or_create(
                followed_by=request.user,
                following=other_user
            )
        else:
            try:
                follower=Follower.objects.get(
                    followed_by=request.user,
                    following=other_user
                )
            except Follower.DoesNotExist:
                follower=None
                
            if follower:
                follower.delete()
        print("before wording-",data["action"])
        return JsonResponse({
            "success":True,
           "wording":"Unfollow" if data["action"] =="follow" else "Follow"
            #first action is "follow" then we followed and text should change to "unfollow" viceversa
            
        }
        )
            

class UpdateProfileView(UpdateView):
    model=Profile
    template_name="profile/update_profile.html"
    fields=['first_name', 'last_name','username','password', 'image']
    success_url='/'
    
    def get_object(self,query_set=None):
        return self.request.user.profile
    
    def form_valid(self, form):
        username=form.cleaned_data['username']
        password=form.cleaned_data['password']
        
        
        # Update user information
        self.request.user.username=username
        if password: 
            self.request.user.set_password(password)
            
            self.request.user.save()
        # # Update session if password changed
            update_session_auth_hash(self.request, self.request.user)
        else:
            self.request.user.save()
            
        return super().form_valid(form)
    
