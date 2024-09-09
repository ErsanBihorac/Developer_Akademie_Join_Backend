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
import json
import datetime
from todolist.models import Contact, TodoItem
from .serializers import ContactSerializer, EmailAuthTokenSerializer, TodoItemSerializer

@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

class ContactsView(APIView):
    def get(self, request):
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        try:
            data = request.data
            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            first_letter = data.get('firstLetter')
            color_id = data.get('colorId')

            if not all([name, email, phone, first_letter, color_id]):
                    return Response({'error': 'Missing required fields'}, status=400)

            contact = Contact(
                name = name,
                email = email,
                phone = phone,
                first_letter = first_letter,
                color_id = color_id
            )

            contact.save()
            serializer = TodoItemSerializer(contact)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)})
        
    def put(self, request, contact_id):
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
        
    def delete(self, request, contact_id):
        try:
            contact = Contact.objects.get(id=contact_id)
            contact.delete()
            return Response({'message': 'Contact deleted successfully'})
        except Contact.DoesNotExist:
            return Response({'error': 'Contact not found'})
        except Exception as e:
            return Response({'error': str(e)})

class TodoItemView(APIView):
    def get(self, request):
        todos = TodoItem.objects.all()
        serializer = TodoItemSerializer(todos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        try:
            data = request.data
            title = data.get('title')
            description = data.get('description')
            due_date = data.get('due_date')
            priority = data.get('priority')
            status = data.get('status')
            assigned_to = data.get('assigned_to', [])
            
            if not all([title, description, due_date, priority, status]):
                return Response({'error': 'Missing required fields'}, status=400)

            todo_item = TodoItem(
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                status=status,
            )

            todo_item.save()

            if assigned_to:
                users = User.objects.filter(email__in=assigned_to)
                todo_item.Assigned_to.set(users)

            serializer = TodoItemSerializer(todo_item)
            return Response(serializer.data, status=201)
        except Exception as e:
            return Response({'error': str(e)})
        
    def put(self, request, task_id):
        try:
            todo_item = TodoItem.objects.get(id=task_id)
            data = request.data

            title = data.get('title', todo_item.title)
            description = data.get('description', todo_item.description)
            priority = data.get('priority', todo_item.priority)
            status = data.get('status', todo_item.status)
            due_date_str = data.get('due_date', todo_item.due_date)

            if due_date_str:
                try:
                    due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date()
                except ValueError:
                    return Response({'error': 'Ungültiges Datumsformat, muss YYYY-MM-DD sein'}, status=400)
            else:
                due_date = todo_item.due_date

            assigned_to = data.get('assigned_to', [])

            todo_item.title = title
            todo_item.description = description
            todo_item.due_date = due_date
            todo_item.priority = priority
            todo_item.status = status

            if assigned_to:
                users = User.objects.filter(username__in=assigned_to)
                todo_item.assigned_to.set(users)

            todo_item.save()

            serializer = TodoItemSerializer(todo_item)
            return Response(serializer.data, status=200)

        except TodoItem.DoesNotExist:
            return Response({'error': 'TodoItem nicht gefunden'}, status=400)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    
    def delete(self, request, task_id):
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
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
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


# Schaltet den CSRF-SChutz aus
# im Frontend sorgt der CSRF schutz dafür dass ich mich nicht anmelden kann 
# in Postman funktioniert alles jedoch einwandfrei, ich habe den Fehler nach vielen Stunden nicht gelöst
#  bekommen und wollte nicht noch mehr stunden damit verwschwenden am Frontend zu arbeiten
@method_decorator(csrf_exempt, name='dispatch') 
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