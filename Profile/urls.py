from django.contrib import admin
from django.urls import path

from .views import ProfileDetailView,FollowView,UpdateProfileView


app_name='profile'
urlpatterns = [
    path("<str:username>/",ProfileDetailView.as_view(),name="detail"),
    path("<str:username>/follow/",FollowView.as_view(),name="follow"),
    path("<int:pk>/update/",UpdateProfileView.as_view(),name='update')

]