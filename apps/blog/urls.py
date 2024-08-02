from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='home'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<str:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<str:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/comments/create/', views.CommentCreateView.as_view(), name='comment_create_view'),
    path('category/<str:slug>/', views.PostFromCategory.as_view(), name='post_by_category'),
]
