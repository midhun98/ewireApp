from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import CustomUser


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128)


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label='Confirm password')

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'password2']

    def validate(self, data):
        if 'username' not in data or not data['username']:
            raise serializers.ValidationError({"username": "This field is required."})

        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")

        # Validate the password for strength
        validate_password(data['password'])

        return data

    def create(self, validated_data):
        user = CustomUser.objects.create(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', ''),
            phone_number=validated_data.get('phone_number', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
