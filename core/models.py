from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from autoslug import AutoSlugField
from taggit.managers import TaggableManager


def create_author(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)


post_save.connect(create_author, sender=User)


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='author_profile_pictures', default="author_profile_pictures/81IBlQyTj3L._AC_SX425_.jpg")
    description = models.TextField()
    facebook = models.URLField()
    twitter = models.URLField()
    instagram = models.URLField()
    youtube = models.URLField()

    def __str__(self):
        return self.user.username


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    slug = AutoSlugField(unique=True, populate_from='title')
    created_at = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author.user.username} on {self.post.title}"

    def get_author_profile_url(self):
        return reverse('core:profile', args=[self.author.user.username])

    def get_replies(self):
        return Comment.objects.filter(parent=self, parent__isnull=False).order_by('created_at')

    @property
    def children(self):
        descendants = []
        for reply in self.replies.all():
            descendants.append(reply)
            descendants.extend(reply.children)
        return descendants

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
