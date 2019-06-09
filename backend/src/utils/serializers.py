from rest_framework import serializers


class EmptySerializer(serializers.Serializer):

    def update(self, instance, validated_data):
        raise NotImplementedError()

    def create(self, validated_data):
        raise NotImplementedError()
