from django.contrib import admin

from webhooks.models import FacebookPage
from webhooks.models import Message
from webhooks.models import Topic


@admin.register(FacebookPage)
class FacebookPageAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'verified']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    ...


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    ...
