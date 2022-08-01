from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import Post
from .filters import PostFilter
from .forms import PostForm


class NewsList(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class PostCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.edit_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DetailView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


class PostSearchView(ListView):
    model = Post
    template_name = 'post_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'
