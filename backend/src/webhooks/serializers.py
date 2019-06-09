from rest_framework import serializers

from webhooks.models import Topic


class TopicSerializer(serializers.ModelSerializer):

     class Meta:
         model = Topic
         fields = '__all__'
         read_only_fields = [
             'id',
             'initiator_id',
             'dialogflow_sessions_id',
             'date_created',
             'source'
         ]