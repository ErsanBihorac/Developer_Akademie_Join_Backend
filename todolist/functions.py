import datetime
import json
from todolist.models import Contact, TodoItem
from rest_framework import serializers
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.http import JsonResponse

@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

def validate_contact_data(data):
    required_fields = ['name', 'email', 'phone', 'firstLetter', 'colorId']
    if not all(data.get(field) for field in required_fields):
        raise ValueError('Missing required fields')

def create_contact(data):
    contact = Contact(
        name=data.get('name'),
        email=data.get('email'),
        phone=data.get('phone'),
        first_letter=data.get('firstLetter'),
        color_id=data.get('colorId')
    )
    contact.save()
    return contact

def serialize_and_respond_contact(contact):
    from todolist.serializers import ContactSerializer
    serializer = ContactSerializer(contact)
    return Response(serializer.data, status=201)

def validate_todo_item_data(data):
    return all([data.get(f) for f in ['title', 'description', 'due_date', 'priority', 'status']])

def create_todo_item(data):
    todo_item = TodoItem(
        title=data.get('title'),
        description=data.get('description'),
        due_date=data.get('due_date'),
        priority=data.get('priority'),
        status=data.get('status'),
    )
    todo_item.save()
    return todo_item

def assign_users_for_todo_item(todo_item, assigned_to):
    if assigned_to:
        users = User.objects.filter(email__in=assigned_to)
        todo_item.Assigned_to.set(users)

def update_todo_item(todo_item, data):
    todo_item.title = data.get('title', todo_item.title)
    todo_item.description = data.get('description', todo_item.description)
    todo_item.priority = data.get('priority', todo_item.priority)
    todo_item.status = data.get('status', todo_item.status)
    todo_item.due_date = parse_due_date(data.get('due_date', todo_item.due_date))
    todo_item.save()
    return todo_item

def update_assigned_users(todo_item, assigned_to):
    if assigned_to:
        users = User.objects.filter(username__in=assigned_to)
        todo_item.assigned_to.set(users)

def parse_due_date(due_date_str):
    try:
        return datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
    except ValueError:
        raise ValueError('Ungültiges Datumsformat, muss YYYY-MM-DD sein')

def get_request_data_of_register(request):
    return json.loads(request.body)

def validate_register_data(data):
    return all([data.get('username'), data.get('email'), data.get('password')])

def create_user(data):
    user = User.objects.create_user(
        username=data['username'], email=data['email'], password=data['password']
    )
    user.save()
    return user

def get_user(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        raise serializers.ValidationError('No user associated with this email.')