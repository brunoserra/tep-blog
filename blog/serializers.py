from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework.reverse import reverse

from .models import *


class PostLinkBuilder(HyperlinkedIdentityField):
    def to_representation(self, value):
        return reverse('post-detail', kwargs={'user_pk': value.user_id, 'post_pk': value.id},
                       request=self.context['request'])


class CommentLinkBuilder(HyperlinkedIdentityField):
    def to_representation(self, value):

        return reverse('comment-detail', kwargs={'user_pk': value.post.user_id, 'post_pk': value.post_id,
                                                 'pk': value.id},
                       request=self.context['request'])


class GeoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ("lat", "lng",)


class AddressSerializer(serializers.ModelSerializer):
    geo = GeoSerializer

    class Meta:
        model = Address
        fields = ("street", "zipcode", "geo",)


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = ("id", "url", "name", "email",)


class ProfileDetailSerializer(serializers.HyperlinkedModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Profile
        fields = ("id", "name", "email", "address",)


class ProfilePostCommentDetailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Comment
        fields = ("id", "name", "email", "body", )


class ProfilePostCommentListSerializer(serializers.HyperlinkedModelSerializer):
    url = CommentLinkBuilder(view_name='comment-detail')

    class Meta:
        model = Comment
        fields = ("url", "id", "name",)


class PostDetailSerializer(serializers.HyperlinkedModelSerializer):
    user = ProfileDetailSerializer
    comments = ProfilePostCommentListSerializer(many=True)

    class Meta:
        model = Post
        fields = ("id", "title", "body", "comments", "user")


class InfoPostListSerializer(serializers.HyperlinkedModelSerializer):
    total_posts = serializers.IntegerField(
        source='posts.count',
        read_only=True
    )

    total_comments = serializers.IntegerField(
        source='comments.count',
        read_only=True
    )

    class Meta:
        model = Profile
        fields = ("id", "name", "total_posts", "total_comments")


class PostSerializer(serializers.HyperlinkedModelSerializer):
    user = ProfileDetailSerializer
    url = PostLinkBuilder(view_name='post-detail')
    comment_count = serializers.IntegerField(
        source='comments.count',
        read_only=True
    )
    comments = ProfilePostCommentListSerializer(many=True)

    class Meta:
        model = Post
        fields = ("url", "id", "title", "body", "comment_count", "comments", "user")


class ProfilePostSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializer(many=True)

    class Meta:
        model = Profile
        fields = ("url", "id", "name", "posts")


class ProfilePostsSerializer(serializers.HyperlinkedModelSerializer):
    posts = PostSerializer(many=True)

    class Meta:
        model = Profile
        fields = ("id", "url", "name", "email", "posts")