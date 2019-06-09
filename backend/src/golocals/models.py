from typing import Optional

from django.contrib.auth import get_user_model
from django.db import models
from django.db import transaction
from ulid import new as ulid

User = get_user_model()


class InitiativeManager(models.QuerySet):
    class VoteSQ(models.Subquery):
        template = "(SELECT * FROM (%(subquery)s) _initiative_vote_value)"
        output_field = models.IntegerField()

    def with_is_starred(self, user):
        inner_qs = StarredInitiative.objects.filter(initiative=models.OuterRef("pk"), user=user)
        return self.annotate(is_starred=models.Exists(inner_qs))

    def with_user_vote(self, user):
        inner_qs = InitiativeVote.objects.filter(
            initiative=models.OuterRef("pk"), user=user
        ).values("value")
        return self.annotate(user_vote=self.VoteSQ(inner_qs))

    def with_comments_count(self):
        return self.annotate(comments_count=models.Count('comment'))

    def filter_for_is_stared(self, user, is_starred: bool):
        inner_qs = StarredInitiative.objects.filter(user=user).values("initiative_id")
        if is_starred:
            return self.filter(id__in=inner_qs)

        return self.exclude(id__in=inner_qs)


class Initiative(models.Model):
    id = models.TextField(primary_key=True, default=ulid)

    title = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_edited = models.DateTimeField(auto_now=True, null=True, blank=True)
    is_edited = models.BooleanField(default=False)

    votes = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)

    author = models.ForeignKey(User, on_delete=models.CASCADE)

    cover = models.URLField(null=True, blank=True, default=None)

    objects = InitiativeManager.as_manager()

    def save(self, *args, **kwargs):
        self.is_edited = True if self.id else False
        super(Initiative, self).save(*args, **kwargs)

        # Add annotated fields so that it won't crash
        # inside serializer just after object is created
        if self._state.adding is True:
            self.is_starred = False
            self.user_vote = None
            self.comments_count = 0

    def vote_up(self, user):
        self._vote(user, 1)

    def vote_down(self, user):
        self._vote(user, -1)

    def remove_vote(self, user):
        vote: Optional[InitiativeVote] = InitiativeVote.objects.filter(
            user=user, initiative=self
        ).first()
        if vote:
            vote.delete()

    @transaction.atomic()
    def _vote(self, user, value):
        created = False
        try:
            vote: InitiativeVote = InitiativeVote.objects.get(user=user, initiative=self)
        except InitiativeVote.DoesNotExist:
            vote = InitiativeVote.objects.create(user=user, initiative=self, value=value)
            created = True

        if created:
            self.votes = models.F("votes") + value
        else:
            if vote.value != value:
                self.votes = models.F("votes") + (value * 2)
                vote.value = value
                vote.save()

        self.save()

    def annotate_fields(self, user):
        self.is_starred = StarredInitiative.objects.filter(user=user, initiative=self).exists()

        self.comments_count = Comment.objects.filter(initiative=self).count()

        _vote = InitiativeVote.objects.filter(user=user, initiative=self).first()
        if _vote:
            self.user_vote = _vote.value
        else:
            self.user_vote = None

    class Meta:
        ordering = ["-date_created"]


class InitiativeVote(models.Model):
    _VALUES = ((1, "up-vote"), (-1, "down-vote"))

    value = models.SmallIntegerField(choices=_VALUES)
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["initiative", "user"]

    @transaction.atomic()
    def delete(self, *args, **kwargs):
        self.initiative.votes = models.F("votes") - self.value
        self.initiative.save()
        super(InitiativeVote, self).delete(*args, **kwargs)


class StarredInitiative(models.Model):
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["initiative", "user"]


class CommentManager(models.QuerySet):
    class VoteSQ(models.Subquery):
        template = "(SELECT * FROM (%(subquery)s) _initiative_vote_value)"
        output_field = models.IntegerField()

    def with_user_vote(self, user):
        inner_qs = CommentVote.objects.filter(
            comment=models.OuterRef("pk"), user=user
        ).values("value")
        return self.annotate(user_vote=self.VoteSQ(inner_qs))


class Comment(models.Model):
    initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    body = models.TextField()

    votes = models.IntegerField(default=0)

    objects = CommentManager.as_manager()

    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('date_created',)

    def vote_up(self, user):
        self._vote(user, 1)

    def vote_down(self, user):
        self._vote(user, -1)

    @transaction.atomic()
    def _vote(self, user, value):
        created = False
        try:
            vote: CommentVote = CommentVote.objects.get(user=user, comment=self)
        except CommentVote.DoesNotExist:
            vote = CommentVote.objects.create(user=user, comment=self, value=value)
            created = True

        if created:
            self.votes = models.F("votes") + value
        else:
            if vote.value != value:
                self.votes = models.F("votes") + (value * 2)
                vote.value = value
                vote.save()

        self.save()

    def annotate_fields(self, user):
        _vote = CommentVote.objects.filter(user=user, comment=self).first()
        if _vote:
            self.user_vote = _vote.value
        else:
            self.user_vote = None

    def save(self, *args, **kwargs):
        super(Comment, self).save(*args, **kwargs)
        if self._state.adding is True:
            self.user_vote = None


    def remove_vote(self, user):
        vote: Optional[CommentVote] = CommentVote.objects.filter(
            user=user, comment=self
        ).first()
        if vote:
            vote.delete()


class CommentVote(models.Model):
    _VALUES = ((1, "up-vote"), (-1, "down-vote"))

    value = models.SmallIntegerField(choices=_VALUES)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["comment", "user"]

    @transaction.atomic()
    def delete(self, *args, **kwargs):
        self.comment.votes = models.F("votes") - self.value
        self.comment.save()
        super().delete(*args, **kwargs)
