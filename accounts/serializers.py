# core Django.
from django.contrib.auth import get_user_model

# third party.
from dj_rest_auth.serializers import UserDetailsSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

User = get_user_model()

class CustomRegisterSerializer(RegisterSerializer):
    # This catches the server error when a user tries to use a registered email address.
    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return email

class OwnerDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        # communities_joined and communities_created are not fields on the User model.
        # They are gotten from the 'related_name' attribute on Foreign key and ManyToMany 
        # fields on the Community model linked to users. 
        fields = ['profile_picture', 'email', 'username', 'bio', 'date_joined', 'communities_created', 'communities_joined']
        model = User

class RandomUserDetailsSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_picture','username', 'bio', 'date_joined', 'communities_joined', 'communities_created']

class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'bio']