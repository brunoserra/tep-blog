from django.http import Http404
from rest_framework.response import Response
from rest_framework.utils import json

from .serializers import *
from rest_framework import generics


class ProfileList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = 'profile-list'
    http_method_names = ['get']


class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    name = 'profile-detail'
    http_method_names = ['get']


class ProfilePostList(generics.ListCreateAPIView):
    name = 'profile-post-list'
    queryset = Profile.objects.all()
    serializer_class = ProfilePostSerializer
    http_method_names = ['post', 'get']

    def get(self, request, user_pk, format=None):
        snippet = Profile.objects.get(id=user_pk)
        serializer = ProfilePostSerializer(snippet, context={'request': request})
        return Response(serializer.data)


class ProfilePostDetail(generics.ListAPIView):
    name = 'post-detail'
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    http_method_names = ['get']

    def get(self, request, user_pk, post_pk, format=None):
        snippet = Post.objects.get(id=post_pk, user_id=user_pk)
        serializer = PostDetailSerializer(snippet, context={'request': request})
        return Response(serializer.data)


class ProfilePostAllList(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfilePostsSerializer
    name = 'profile-post-all'
    http_method_names = ['get']


class ProfilePostCommentList(generics.ListAPIView):
    name = 'comment-list'
    queryset = Comment.objects.all()
    serializer_class = ProfilePostCommentListSerializer
    http_method_names = ['get']

    def get(self, request, user_pk, post_pk, format=None):
        snippet = Comment.objects.all().filter(post_id=post_pk).prefetch_related('post', 'post__user')
        serializer = ProfilePostCommentListSerializer(snippet, many=True, context={'request': request})
        return Response(serializer.data)


class ProfilePostCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = ProfilePostCommentDetailSerializer
    name = 'comment-detail'

    def get(self, request, user_pk, post_pk, pk, format=None):
        snippet = Comment.objects.get(id=pk, post_id=post_pk, post__user_id=user_pk)
        serializer = ProfilePostCommentDetailSerializer(snippet, many=False, context={'request': request})
        return Response(serializer.data)


class InfoPostList(generics.ListAPIView):
    name = 'info-post-list'
    queryset = Profile.objects.all()
    serializer_class = InfoPostListSerializer
    http_method_names = ['get']


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return Response({
            'profiles': reverse(ProfileList.name, request=request),
            'posts': reverse(ProfilePostAllList.name, request=request),
            'info-posts': reverse(InfoPostList.name, request=request),
         })
