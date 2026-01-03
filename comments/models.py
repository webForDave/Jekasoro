from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth import get_user_model 

from posts.models import Post

User = get_user_model()

class Comment(models.Model):
    content = models.TextField()
    up_voters = models.ManyToManyField(User, related_name='upvoted_comments')
    down_voters = models.ManyToManyField(User, blank=True, related_name='downvoted_comments')
    vote_count = models.IntegerField(default=0)
    comment_author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    slug = AutoSlugField(populate_from='content', unique=True, overwrite=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']