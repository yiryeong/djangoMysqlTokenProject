from rest_framework import serializers
from payhistory.models import User, PayHistory
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # make_password 이용해 단방향 암호화 비밀번호를 구현
        validated_data['password'] = make_password(validated_data['password'])
        user = User.objects.create(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('email', 'password')


class HistorySerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        history = PayHistory.objects.create(**validated_data)
        return history

    class Meta:
        model = PayHistory
        fields = ('datetime', 'price', 'memo', 'uid')
        # fields = '__all__'
