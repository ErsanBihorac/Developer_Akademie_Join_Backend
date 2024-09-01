from django.shortcuts import render
from django.views import View
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from rest_framework import status
from .serializers import EmailAuthTokenSerializer
# Create your views here.

@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

class LoginView(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'message': 'Login erfolgreich',
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        }, status=status.HTTP_200_OK)

class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')

            if not username or not email or not password:
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            return JsonResponse({'message': 'User created successfully'}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)