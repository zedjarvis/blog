from . import views
from django.urls import path


urlpatterns = [
    path('', views.blogHome, name='home'),
    path('<slug:slug>/', views.postDetail, name='post_detail'),
]
