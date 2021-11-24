from rest_framework import serializers
from payhistory.models import PayHistory
from django.contrib.auth.hashers import make_password


class HistorySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        history = PayHistory.objects.create(**validated_data)
        return history

    class Meta:
        model = PayHistory
        fields = ('datetime', 'price', 'memo', 'uid')
        # fields = '__all__'
