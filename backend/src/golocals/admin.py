from django.contrib import admin

from golocals.models import Comment
from golocals.models import CommentVote
from golocals.models import Initiative
from golocals.models import InitiativeVote
from golocals.models import StarredInitiative


@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date_created']


@admin.register(InitiativeVote)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ['id', 'value', 'initiative', 'user']


@admin.register(StarredInitiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ['id', 'initiative', 'user']


@admin.register(Comment)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ['id', 'initiative', 'user', 'votes', 'date_created']


@admin.register(CommentVote)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ['id', 'value', 'comment', 'user']
