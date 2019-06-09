import json
from json import JSONDecodeError

from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet

from golocals.models import Comment
from golocals.models import Initiative
from golocals.models import StarredInitiative
from golocals.serializers import CommentSerializer
from golocals.serializers import InitiativeCreateSerializer
from golocals.serializers import InitiativeReadOnlySerializer


class StarredInitiativesFilter(BaseFilterBackend):
    param_name = "starred"

    def filter_queryset(self, request, queryset, view):
        param_value = request.query_params.get(self.param_name)
        if not param_value:
            return queryset

        try:
            value = bool(json.loads(param_value))
        except JSONDecodeError:
            raise ValidationError(
                {
                    api_settings.NON_FIELD_ERRORS_KEY: (
                        "Invalid value for `liked-only` query parameter. "
                        "Only number is allowed"
                    )
                }
            )

        return queryset.filter_for_is_stared(request.user, value)


class InitiativesAPI(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, GenericViewSet):
    queryset = Initiative.objects.none()
    serializer_class = InitiativeReadOnlySerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (StarredInitiativesFilter,)

    def get_queryset(self):
        return (
            Initiative.objects
                .with_is_starred(self.request.user)
                .with_user_vote(self.request.user)
                .with_comments_count()
        )

    def get_serializer_class(self):
        if self.action in ("list", "retrieve", "upvote", "downvote", "removevote"):
            return InitiativeReadOnlySerializer
        if self.action == "create":
            return InitiativeCreateSerializer

        return self.serializer_class

    @action(["POST", "DELETE"], detail=True)
    def star(self, request, *args, **kwargs):
        if request.method == "POST":
            return self._favourite_post()
        elif request.method == "DELETE":
            return self._favourite_delete()

        raise RuntimeError("Unexpected branch")

    def _favourite_post(self):
        initiative = self.get_object()
        StarredInitiative.objects.get_or_create(topic=initiative, user=self.request.user)
        return Response(status=status.HTTP_202_ACCEPTED)

    def _favourite_delete(self):
        initiative = self.get_object()
        StarredInitiative.objects.filter(topic=initiative, user=self.request.user).delete()
        return Response(status=status.HTTP_202_ACCEPTED)

    @action(["POST"], detail=True)
    def upvote(self, *args, **kwargs):
        topic = self.get_object()
        topic.vote_up(self.request.user)
        topic.refresh_from_db()
        topic.annotate_fields(self.request.user)
        sr = self.get_serializer_class()(topic)
        return Response(sr.data, status=status.HTTP_200_OK)

    @action(["POST"], detail=True)
    def downvote(self, *args, **kwargs):
        topic = self.get_object()
        topic.vote_down(self.request.user)
        topic.refresh_from_db()
        topic.annotate_fields(self.request.user)
        sr = self.get_serializer_class()(topic)
        return Response(sr.data, status=status.HTTP_200_OK)

    @action(["POST"], detail=True)
    def removevote(self, *args, **kwargs):
        topic = self.get_object()
        topic.remove_vote(self.request.user)
        topic.refresh_from_db()
        topic.annotate_fields(self.request.user)
        sr = self.get_serializer_class()(topic)
        return Response(sr.data, status=status.HTTP_200_OK)


class CommentsAPI(ModelViewSet):
    """
    To filter by initiative user following query param:
    ```
    ?initiative_id=abc
    ```
    """
    queryset = Comment.objects.none()
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('initiative_id',)

    def get_serializer_class(self):
        return CommentSerializer

    def get_queryset(self):
        return Comment.objects.with_user_vote(user=self.request.user)

    @action(["POST"], detail=True)
    def upvote(self, *args, **kwargs):
        comment: Comment = self.get_object()
        comment.vote_up(self.request.user)
        comment.refresh_from_db()
        comment.annotate_fields(self.request.user)
        sr = self.get_serializer_class()(comment)
        return Response(sr.data, status=status.HTTP_200_OK)

    @action(["POST"], detail=True)
    def downvote(self, *args, **kwargs):
        comment: Comment = self.get_object()
        comment.vote_down(self.request.user)
        comment.refresh_from_db()
        comment.annotate_fields(self.request.user)
        sr = self.get_serializer_class()(comment)
        return Response(sr.data, status=status.HTTP_200_OK)

    @action(["POST"], detail=True)
    def removevote(self, *args, **kwargs):
        comment: Comment = self.get_object()
        comment.remove_vote(self.request.user)
        comment.refresh_from_db()
        comment.annotate_fields(self.request.user)
        sr = self.get_serializer_class()(comment)
        return Response(sr.data, status=status.HTTP_200_OK)
