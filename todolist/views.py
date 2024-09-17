from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from todolist.models import Contact, TodoItem
from .serializers import ContactSerializer, EmailAuthTokenSerializer, TodoItemSerializer
from .functions import (
    create_contact, serialize_and_respond_contact,
    validate_todo_item_data, create_todo_item, assign_users_for_todo_item,
    update_todo_item, update_assigned_users,
    get_request_data_of_register, validate_register_data, create_user
)

class ContactsView(APIView):
    def get(self, request, *args, **kwargs):
        """
        This function returns all contacts.
        """
        try:
            contacts = Contact.objects.all()
            serializer = ContactSerializer(contacts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        """
        This function adds new contacts
        """
        try:
            data = request.data
            contact = create_contact(data)
            return serialize_and_respond_contact(contact)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    def put(self, request, contact_id, *args, **kwargs):
        """
        This function updates a specific contact
        """
        try:
            contact = Contact.objects.get(id=contact_id)
            serializer = ContactSerializer(contact, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=200)
            else:
                return Response(serializer.errors, status=200)
            
        except Exception as e:
            return Response({'error': str(e)}, status=500)
        
    def delete(self, request, contact_id, *args, **kwargs):
        """
        This function deletes a specific contact
        """
        try:
            contact = Contact.objects.get(id=contact_id)
            contact.delete()
            return Response({'message': 'Contact deleted successfully'})
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found'})
        except Exception as e:
            return Response({'error': str(e)})

class TodoItemView(APIView):
    def get(self, request, *args, **kwargs):
        """
        This function returns the todo items
        """
        try:
            todos = TodoItem.objects.all()
            serializer = TodoItemSerializer(todos, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def post(self, request, *args, **kwargs):
        """
        This function adds new todo items
        """
        try:
            data = request.data
            if not validate_todo_item_data(data):
                return Response({'error': 'Missing required fields'}, status=400)
            todo_item = create_todo_item(data)
            assign_users_for_todo_item(todo_item, data.get('assigned_to', []))
            serializer = TodoItemSerializer(todo_item)
            return Response(serializer.data, status=201)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def put(self, request, task_id, *args, **kwargs):
        """
        This function updates a specific todo items
        """
        try:
            todo_item = TodoItem.objects.get(id=task_id)
            data = request.data

            todo_item = update_todo_item(todo_item, data)
            update_assigned_users(todo_item, data.get('assigned_to', []))

            serializer = TodoItemSerializer(todo_item)
            return Response(serializer.data, status=200)
        except TodoItem.DoesNotExist:
            return Response({'error': 'TodoItem nicht gefunden'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def delete(self, request, task_id, *args, **kwargs):
        """
        This function delets a specific todo item
        """
        try:
            todos = TodoItem.objects.get(id=task_id)
            todos.delete()
            return Response({'message': 'Task deleted successfully'})
        except TodoItem.DoesNotExist:
            return Response({'error': 'Task not found'})
        except Exception as e:
            return Response({'error': str(e)}, status=500)

class LoginView(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        """
        this functions logs the user in
        """
        try:
            serializer = self.serializer_class(data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'message': 'Login erfolgreich',
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'username': user.username
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=500)


# This disables the CSRF guard, i had issues in the frontend with it so i disabled it. But enabled it works fine with postman, just make sure to get your csrf token correct url and then send it with the registration
@method_decorator(csrf_exempt, name='dispatch') 
class RegisterView(View):
    """
    This function registers a new user
    """
    def post(self, request, *args, **kwargs):
        try:
            data = get_request_data_of_register(request)
            if not validate_register_data(data):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'error': 'Email already exists'}, status=400)
    
            create_user(data)
            return JsonResponse({'message': 'User created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)