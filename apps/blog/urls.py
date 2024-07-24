from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('post/<str:slug>/', views.PostDetailView.as_view(), name='post_detail'),
]
