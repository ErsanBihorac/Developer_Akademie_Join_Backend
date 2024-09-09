from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Contact, TodoItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ContactSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
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
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError('No user associated with this email.')

            if not user.check_password(password):
                raise serializers.ValidationError('Incorrect password.')
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

        attrs['user'] = user
        return attrs