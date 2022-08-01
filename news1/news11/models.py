from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)

    def update_rating(self):
        self.user_rating = self.user_rating * 3 + Post.a_or_n_rating + Comment.comment_rating
        return self.user_rating


class Category(models.Model):
    category_name = models.CharField(unique=True, max_length=255)

    def __str__(self):
        return self.category_name.title()


class Post(models.Model):
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE)
    article_or_news = models.BooleanField(default=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255, default='Заголовок')
    a_or_n_text = models.TextField()
    a_or_n_rating = models.IntegerField(default=0)

    def like(self):
        self.a_or_n_rating = self.a_or_n_rating + 1
        return self.a_or_n_rating

    def dislike(self):
        self.a_or_n_rating = self.a_or_n_rating - 1
        return self.a_or_n_rating

    def preview(self):
        return self.a_or_n_text.split()[12]

    def __str__(self):
        return f'{self.header.title()}: {self.a_or_n_text[:20]}'

    def get_absolute_url(self):
        return f'/news/{self.id}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    comment_time = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating = self.comment_rating + 1
        return self.comment_rating

    def dislike(self):
        self.comment_rating = self.comment_rating - 1
        return self.comment_rating

    def __str__(self):
        return self.comment.title()
