"""
Serializers for the API view.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""
    password2 = serializers.CharField(max_length=255, write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'password2', 'name']
        # extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({'detail': 'passwords does not match!'})
        
        try:
            validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': list(e.messages)})
            
        return super().validate(attrs)
    
    def create(self, validated_data):
       """Create and return a user with encrypted password."""
       validated_data.pop('password2', None)
       return get_user_model().objects.create_user(**validated_data)
   
    def update(self, instance, validated_data):
        """Update and return a user."""
        password = validated_data.pop('password', None)
        user =  super().update(instance, validated_data)
        
        if password:
            user.set_password(password)
            user.save()
            
        return user
    

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )
    
    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs