from django.urls import path
from .views import NewsList, PostDetailView, PostCreateView, PostDeleteView, PostSearchView, PostUpdateView

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', PostDetailView.as_view()),
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('search/', PostSearchView.as_view(), name='post_search'),
    path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
    path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]