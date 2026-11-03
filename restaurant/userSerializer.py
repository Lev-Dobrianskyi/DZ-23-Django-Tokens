from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user


class ProfileSerializer(serializers.Serializer):
    message = serializers.CharField()
    username = serializers.CharField()
    user_id = serializers.IntegerField()
