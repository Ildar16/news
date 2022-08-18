from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import send_mail, EmailMultiAlternatives
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.template.loader import render_to_string
from django.core.cache import cache
from .models import Post, Category, CategorySubscribers
from .filters import PostFilter
from .forms import PostForm
from .tasks import email_task


class NewsList(ListView):
    model = Post
    ordering = 'creation_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


class PostCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.add_post',)


class PostUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    template_name = 'post_create.html'
    form_class = PostForm
    permission_required = ('news.edit_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    permission_required = ('news.delete_post',)
    success_url = '/news/'


class PostSearchView(ListView):
    model = Post
    template_name = 'post_search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post_detail'
    queryset = Post.objects.all()


class CategoryList(ListView):
    model = Category
    template_name = 'news/category_list.html'
    context_object_name = 'categories'


class CategoryDetail(DetailView):
    template_name = 'news/category_subscription.html'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs.get('pk')
        category_subscribers = Category.objects.filter(pk=category_id).values("subscribers__username")
        context['is_not_subscribe'] = not category_subscribers.filter(subscribers__username=self.request.user).exists()
        context['is_subscribe'] = category_subscribers.filter(subscribers__username=self.request.user).exists()
        return context


@login_required
def add_subscribe(request, **kwargs):
    pk = request.GET.get('pk', )
    print('Пользователь', request.user, 'добавлен в подписчики категории:', Category.objects.get(pk=pk))
    Category.objects.get(pk=pk).subscribers.add(request.user)
    return redirect('/posts/categories')


def sending_emails_to_subscribers(instance):
    sub_text = instance.a_or_n_text
    sub_title = instance.header
    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).category.pk)
    subscribers = category.subscribers.all()

    for subscriber in subscribers:
        subscriber_username = subscriber.username
        subscriber_useremail = subscriber.email
        html_content = render_to_string('news/mail.html',
                                        {'user': subscriber,
                                         'title': sub_title,
                                         'text': sub_text[:50],
                                         'post': instance})
        email_task(subscriber_username, subscriber_useremail, html_content)
    return redirect('/posts/')


def post(self, request, *args, **kwargs):
    form = PostForm(request.POST)
    post_category_pk = request.POST['post_category']
    sub_text = request.POST.get('text')
    sub_title = request.POST.get('title')
    post_category = Category.objects.get(pk=post_category_pk)
    subscribers = post_category.subscribers.all()
    host = request.META.get('HTTP_HOST')

    if form.is_valid():
        news = form.save(commit=False)
        news.save()

    for subscriber in subscribers:
        html_content = render_to_string(
            'news/mail_sender.html',
            {'user': subscriber, 'text': sub_text[:50], 'post': news, 'title': sub_title, 'host': host})
        html_content = render_to_string(
            'news/mail.html',
            {'user': subscriber, 'text': sub_text[:50], 'post': news, 'title': sub_title, 'host': host}
        )

        msg = EmailMultiAlternatives(
            subject=f'Здравствуй, {subscriber.username}. Новая статья в вашем разделе!',
            body=f'{sub_text[:50]}',
            from_email='ildark116@yandex.ru',
            to=[subscriber.email],
        )

        msg.attach_alternative(html_content, "text/html")
    return redirect('/posts/')
