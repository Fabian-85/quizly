from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):

    """
    Serializer for registering a new user.
    Validates that the email is unique and saves the user with a hashed password.
    username, password, and email are required fields.
    username must be unique.
    """

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'email': {'required': True}}
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use")
        return value
    
    def save(self):
        pw = self.validated_data['password']
        account = User(username=self.validated_data['username'],email=self.validated_data['email'])
        account.set_password(pw)
        account.save()
        return account