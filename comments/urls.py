from django.urls import path
from . import views

urlpatterns = [
    path('', views.comment_view_create, name='post_comments'),
    path('<int:comment_id>/', views.comment_details, name='comment_details'),
    path('<int:comment_id>/upvote/', views.upvote_comment, name='upvote_comment'),
    path('<int:comment_id>/downvote/', views.downvote_comment, name='downvote_comment'),
    path('<int:comment_id>/remove-vote/', views.remove_vote_on_comment, name='remove_comment_vote'),
    path('<int:comment_id>/replies/', views.replies_view_create, name='comment_replies'),
]