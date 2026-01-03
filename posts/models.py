from django.db import models
from django_extensions.db.fields import AutoSlugField
from django.contrib.auth import get_user_model
from communities.models import Community
User = get_user_model()

class Post(models.Model):
    title = models.CharField(unique=True, max_length=50, null=False, blank=False)
    content = models.TextField()
    up_voters = models.ManyToManyField(User, related_name='upvoted_posts')
    down_voters = models.ManyToManyField(User, blank=True, related_name='downvoted_posts')
    vote_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='posts_created')
    slug = AutoSlugField(populate_from='title', unique=True, overwrite=False)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='community_posts')
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.title