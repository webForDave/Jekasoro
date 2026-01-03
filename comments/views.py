# third party Django
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# app level
from .models import Comment
from posts.models import Post
from communities.models import Community
from .serializers import (
    CreateCommentSerializer, 
    PostCommentsSerializer, 
    UpdateCommentSerializer,
    CommentRepliesSerializer,
)

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_view_create(request, community_slug, post_slug):
    try:
        community = Community.objects.get(slug__iexact=community_slug)
    except Community.DoesNotExist:
        return Response({'communities': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        post = Post.objects.get(slug=post_slug)
    except Post.DoesNotExist:
        return Response({'posts': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostCommentsSerializer(post.post_comments, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = CreateCommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(post_id=post.id, comment_author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def comment_details(request, community_slug, post_slug, comment_id):

    try:
        Community.objects.get(slug__iexact=community_slug)
    except Community.DoesNotExist:
        return Response({'communities': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        Post.objects.get(slug__iexact=post_slug)
    except Post.DoesNotExist:
        return Response({'posts': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({'comments': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PostCommentsSerializer(comment)
        return Response(serializer.data)
    
    if request.user != comment.comment_author:
        return Response({'comments': 'You do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT':
        serializer = UpdateCommentSerializer(comment, data=request.data)

        if serializer.is_valid():
            serializer.save(comment_author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        

@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def upvote_comment(request, community_slug, post_slug, comment_id):

    try:
        Community.objects.get(slug__iexact=community_slug)
    except Community.DoesNotExist:
        return Response({'communities': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        post = Post.objects.get(slug=post_slug)
    except Post.DoesNotExist:
        return Response({'posts': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({'comments': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if request.user in comment.up_voters.all():
            return Response({'comments': 'You already casted a vote on this comment'})
        else:
            if request.user in comment.down_voters.all():
                comment.down_voters.remove(request.user)
            comment.up_voters.add(request.user)
            comment.vote_count = len(comment.up_voters.all()) - len(comment.down_voters.all())
            comment.save()
            return Response({'comment': 'voted'})
    
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def downvote_comment(request, community_slug, post_slug, comment_id):

    try:
        Community.objects.get(slug__iexact=community_slug)
    except Community.DoesNotExist:
        return Response({'communities': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        post = Post.objects.get(slug=post_slug)
    except Post.DoesNotExist:
        return Response({'posts': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({'comments': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if request.user in comment.down_voters.all():
            return Response({'comments': 'You already casted a vote on this comment'})
        else:
            if request.user in comment.up_voters.all():
                comment.up_voters.remove(request.user)
            comment.down_voters.add(request.user)
            comment.vote_count = len(comment.up_voters.all()) - len(comment.down_voters.all())

            comment.save()
            return Response({'comment': 'voted'})
        
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def remove_vote_on_comment(request, community_slug, post_slug, comment_id):

    try:
        Community.objects.get(slug__iexact=community_slug)
    except Community.DoesNotExist:
        return Response({'communities': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        post = Post.objects.get(slug=post_slug)
    except Post.DoesNotExist:
        return Response({'posts': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({'comments': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        if request.user in comment.down_voters.all():
            comment.down_voters.remove(request.user)
        elif request.user in comment.up_voters.all():
            comment.up_voters.remove(request.user)
        comment.vote_count = len(comment.up_voters.all()) - len(comment.down_voters.all())
        comment.save()
        return Response({'post': 'success'})
    

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def replies_view_create(request, community_slug, post_slug, comment_id):
    try:
        Community.objects.get(slug__iexact=community_slug)
    except Community.DoesNotExist:
        return Response({'communities': 'Community not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        post = Post.objects.get(slug__iexact=post_slug)
    except Post.DoesNotExist:
        return Response({'posts': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({'comments': 'Comment not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET': 
        serializer = CommentRepliesSerializer(comment.replies, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CreateCommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(post_id=post.id, comment_author=request.user)
            child_comment = Comment.objects.get(content=serializer.validated_data['content'])
            child_comment.parent = comment
            child_comment.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    if request.user != comment.comment_author:
        return Response({'comments': 'You do not have permission to perform this action'}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'PUT':
        serializer = serializer = CreateCommentSerializer(comment, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)