from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

article = 'A'
news = 'N'
TYPES = [
    (article, 'Статья'),
    (news, 'Новость')
]


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=1, choices=TYPES, default=article)
    some_datetime = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=55)
    article_text = models.TextField()
    rating_post = models.IntegerField(default=0)
    description = models.TextField()

    def preview(self):
        return f'{self.description[0:124]}...'

    def like(self):
        self.rating_post += 1
        self.save()

    def dislike(self):
        self.rating_post -= 1
        self.save()


class PostCategory(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    categories = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.CharField(max_length=555)
    datetime = models.DateTimeField(auto_now_add=True)
    rating_comments = models.IntegerField()

    def like(self):
        self.rating_comments += 1
        self.save()

    def dislike(self):
        self.rating_comments -= 1
        self.save()

    def __str__(self):
        return f'{self.user}:{self.comments}'


class Author(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating_post = 0
        for post in self.name.all():
            self.rating_post += post.rating * 3
            for other_comment in post.comment_set.exclude(author_username=self.user.username):
                self.rating_post += other_comment.rating
        for comment in self.user.comment_set.all():
            self.rating_post += comment.rating_comments
        self.save()
