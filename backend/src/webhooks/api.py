# import itertools
# from django.db import transaction
# from django.http import HttpResponse
# from rest_framework.exceptions import ValidationError
# from rest_framework.response import Response
# from rest_framework.viewsets import GenericViewSet
# from rest_framework.viewsets import ModelViewSet
#
# from utils.serializers import EmptySerializer
# from webhooks.dialogflow import talk_to_assistant
# from webhooks.messenger import send_message
# from webhooks.models import FacebookPage
# from webhooks.models import Message
# from webhooks.models import Topic
# from webhooks.serializers import TopicSerializer
#
#
# class FacebookWebHookAPI(GenericViewSet):
#     serializer_class = EmptySerializer
#
#     def get_queryset(self):
#         """
#         Stub get queryset. Just to make router work
#         """
#         return FacebookPage.objects.none()
#
#     def list(self, request, *args, **kwargs):
#         """
#         Verification Endpoint.
#         """
#         challenge = request.GET.get("hub.challenge")
#         verify_token = request.GET.get("hub.verify_token")
#
#         page: FacebookPage = FacebookPage.objects.filter(verify_token=verify_token).first()
#         if not page:
#             raise ValidationError("Invliad token. Page not found.")
#
#         if not page.verify_token.strip() == verify_token.strip():
#             raise ValidationError("Page for given token not found.")
#
#         page.set_as_verified()
#         return HttpResponse(challenge.encode())
#
#     def create(self, request, *args, **kwargs):
#         entry = request.data['entry']
#         all_messaging = [obj['messaging'] for obj in entry]
#         messages = itertools.chain(*all_messaging)
#
#         for msg in messages:
#             self.handle_message(msg)
#
#         return Response(status=204)
#
#     @transaction.atomic()
#     def handle_message(self, msg):
#         content = msg['message']
#         sender_id = msg['sender']['id']
#         if not content:
#             return
#
#         if content.get('is_echo'):
#             return
#
#         if content.get('attachments'):
#             ...
#
#         # FB can send message multiple times, mid can be used to check duplicates
#         # message['mid']
#
#         text = content.get('text')
#
#         topic: Topic
#         topic, _ = Topic.objects.get_or_create(initiator_id=sender_id)
#
#         Message.objects.create(
#             topic=topic,
#             text=text,
#             is_author_consultant=False,
#             is_author_bot=False,
#             is_author_customer=True,
#         )
#
#         if not topic.dialogflow_sessions_id:
#             topic.set_dialogflow_session_id()
#
#         bot_response = talk_to_assistant(text, topic.dialogflow_sessions_id)
#
#         Message.objects.create(
#             topic=topic,
#             text=bot_response,
#             is_author_consultant=False,
#             is_author_bot=True,
#             is_author_customer=False,
#         )
#
#         # TODO
#         page: FacebookPage = FacebookPage.objects.first()
#         send_message(page.page_access_token, sender_id, bot_response)
#
#         print('Got message:', msg)
#
#
# class TopicAPI(ModelViewSet):
#     queryset = Topic.objects.all()
#     serializer_class = TopicSerializer
