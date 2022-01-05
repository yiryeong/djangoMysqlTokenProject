from rest_framework import serializers
from user.models import User
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
