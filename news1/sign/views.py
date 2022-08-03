from django.shortcuts import render

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from news11.models import Author


class AuthorGroup(PermissionRequiredMixin, CreateView):
    permission_required = ('sign.add_post', 'change.add_post')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
    return redirect('/')


@login_required
def not_author(request):
    user = request.user
    user_id = request.user.pk
    print(user_id)
    author_delete = Author.objects.get(author_user=user)
    authors_group = Group.objects.get(name='authors')
    if request.user.groups.filter(name='authors').exists():
        authors_group.user_set.remove(user)
        author_delete.delete()
    return redirect('/account/profile/')
