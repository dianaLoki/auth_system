from django.urls import path
from access.views import ArticleListView, ArticleCreateView, ArticleDeleteView, UserListView

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article-list'),
    path('articles/create/', ArticleCreateView.as_view(), name='article-create'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article-delete'),
    path('users/', UserListView.as_view(), name='user-list'),
]