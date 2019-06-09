from django.contrib.auth import get_user_model
from rest_framework import serializers

from golocals.models import Comment
from golocals.models import Initiative

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "badge"]
        read_only_fields = fields


class InitiativeReadOnlySerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    is_starred = serializers.BooleanField()
    user_vote = serializers.IntegerField()
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Initiative
        fields = [
            "id",
            "title",
            "body",
            "date_created",
            "date_edited",
            "is_edited",
            "votes",
            "shares_count",
            "comments_count",
            "author",
            "cover",
            "is_starred",
            "user_vote",
        ]
        read_only_fields = fields


class InitiativeCreateSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    is_starred = serializers.BooleanField(read_only=True)
    user_vote = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Initiative
        fields = [
            "id",
            "title",
            "body",
            "date_created",
            "date_edited",
            "is_edited",
            "votes",
            "author",
            "is_starred",
            "user_vote",
            "cover",
            "shares_count",
            "comments_count",
        ]
        read_only_fields = [
            "id",
            "date_created",
            "date_edited",
            "is_edited",
            "author",
            "is_starred",
            "votes",
            "cover",
            "comments_count",
            "user_vote",
        ]

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user
        return super(InitiativeCreateSerializer, self).create(validated_data)


class CommentSerializer(serializers.ModelSerializer):
    initiative_id = serializers.CharField()
    user = AuthorSerializer(read_only=True)
    user_vote = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'initiative_id',
            'user',
            'body',
            'votes',
            'date_created',
            'user_vote'
        ]
        read_only_fields = ['id', 'user', 'votes', 'date_created', 'user_vote']

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data['user'] = user
        return super(CommentSerializer, self).create(validated_data)
