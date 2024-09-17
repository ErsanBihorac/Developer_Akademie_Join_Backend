from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Contact, TodoItem
from .functions import (get_user)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class TodoItemSerializer(serializers.ModelSerializer):
    assigned_to = UserSerializer(many=True)
    class Meta:
        model = TodoItem
        fields = '__all__'

class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(trim_whitespace=False)

    def validate(self, attrs):
        email, password = attrs.get('email'), attrs.get('password')
        if not email or not password:
            raise serializers.ValidationError('Must include "email" and "password".')
    
        user = get_user(email)
        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password.')
    
        attrs['user'] = user
        return attrs