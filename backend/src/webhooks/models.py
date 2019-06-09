# from uuid import uuid4
#
# from django.contrib.auth import get_user_model
# from django.contrib.postgres.fields import ArrayField
# from django.db import models
#
# User = get_user_model()
#
#
# class FacebookPage(models.Model):
#     name = models.TextField(max_length=300)
#     verify_token = models.TextField(max_length=300, unique=True)
#     verified = models.BooleanField(default=False)
#     page_access_token = models.TextField()
#
#     def set_as_verified(self, save=True):
#         self.verified = True
#         if save:
#             self.save()
#
#
# class Topic(models.Model):
#     SOURCE_CHOICES = (
#         ('fb', 'fb'),
#         ('email', 'email'),
#         ('app', 'app'),
#     )
#
#     initiator_id = models.TextField(unique=True)
#     dialogflow_sessions_id = models.TextField(null=True, blank=True)
#     date_created = models.DateTimeField(auto_now_add=True)
#
#     priority = models.IntegerField(default=0)
#     is_manual_intervention = models.BooleanField(default=False)
#     source = models.CharField(choices=SOURCE_CHOICES, default='app', max_length=255)
#     labels = ArrayField(models.CharField(max_length=255), default=list)
#
#     is_archived = models.BooleanField(default=False)
#
#     def set_dialogflow_session_id(self, save=True):
#         self.dialogflow_sessions_id = str(uuid4()).replace('-', '')
#
#         if save:
#             self.save()
#
#
# class Message(models.Model):
#     topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
#     text = models.TextField()
#
#     is_author_consultant = models.BooleanField()
#     is_author_customer = models.BooleanField()
#     is_author_bot = models.BooleanField()
#
#     consultant = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
#
#     date_created = models.DateTimeField(auto_now_add=True)
