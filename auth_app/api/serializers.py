from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):

    """
    Serializer for registering a new user.
    Validates that the email is unique and saves the user with a hashed password,
    if password and confirmed_password are the same.
    username, password, and email are required fields.
    username must be unique.
    """

    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username' , 'email', 'password','confirmed_password']
        extra_kwargs = {
            'email': {'required': True},
            'password':{'write_only': True}
            }
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use")
        return value
    
    def validate_confirmed_password(self, value):
        password = self.initial_data.get('password')
        if password and value and password != value:
            raise serializers.ValidationError('Passwords do not match')
        return value
    
    def save(self):
        pw = self.validated_data['password']
        account = User(username=self.validated_data['username'],email=self.validated_data['email'])
        account.set_password(pw)
        account.save()
        return account