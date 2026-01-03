from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_view_create, name='post_view_create'),
    path('<slug:post_slug>/', views.post_details, name='post_details'),
    path('<slug:post_slug>/upvote/', views.upvote_post, name='upvote_post'),
    path('<slug:post_slug>/downvote/', views.downvote_post, name='downvote_post'),
    path('<slug:post_slug>/remove-vote/', views.remove_vote_on_post, name='remove_post_vote'),
]