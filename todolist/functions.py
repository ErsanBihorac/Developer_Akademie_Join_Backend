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
    """
    This function returns a csrf token that is needed to register and login
    """
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

def normalize_contact_data(data):
    """
    This function normalizes the contact data by handling both first_letter/color_id and firstLetter/colorId.
    """
    if 'first_letter' in data:
        data['firstLetter'] = data.pop('first_letter')

    if 'color_id' in data:
        data['colorId'] = data.pop('color_id')

    return data

def validate_contact_data(data):
    """
    This function validates the contact data fields
    """
    required_fields = ['name', 'email', 'phone', 'firstLetter', 'colorId']
    if not all(data.get(field) for field in required_fields):
        raise ValueError('Missing required fields')

def create_contact(data):
    """
    This function creates a contact and returns it
    """
    data = normalize_contact_data(data)
    validate_contact_data(data)

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
    """
    This function serializes the contact and returns a response
    """
    from todolist.serializers import ContactSerializer
    serializer = ContactSerializer(contact)
    return Response(serializer.data, status=201)

def validate_todo_item_data(data):
    """
    This function validates the data fields for the todo item
    """
    return all([data.get(f) for f in ['title', 'description', 'due_date', 'priority', 'status']])

def create_todo_item(data):
    """
    This function creates a todo item and returns the todo item
    """
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
    """
    This function assigns users to the todo item
    """
    if assigned_to:
        users = User.objects.filter(email__in=assigned_to)
        todo_item.assigned_to.set(users)

def update_todo_item(todo_item, data):
    """
    This function updates the todo item data fields with new values and returns the todo item
    """
    todo_item.title = data.get('title', todo_item.title)
    todo_item.description = data.get('description', todo_item.description)
    todo_item.priority = data.get('priority', todo_item.priority)
    todo_item.status = data.get('status', todo_item.status)
    todo_item.due_date = parse_due_date(data.get('due_date', todo_item.due_date))
    todo_item.save()
    return todo_item

def update_assigned_users(todo_item, assigned_to):
    """
    This function updates the assigned users of the todo item
    """
    if assigned_to:
        users = User.objects.filter(username__in=assigned_to)
        todo_item.assigned_to.set(users)

def parse_due_date(due_date_str):
    """
    This function parses the date of the due date fields and returns the value
    """
    try:
        return datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
    except ValueError:
        raise ValueError('Ungültiges Datumsformat, muss YYYY-MM-DD sein')

def get_request_data_of_register(request):
    """
    This function returns the parsed data from the request
    """
    return json.loads(request.body)

def validate_register_data(data):
    """
    This function validates and returns the data fields from the register
    """
    return all([data.get('username'), data.get('email'), data.get('password')])

def create_user(data):
    """
    This function creates a new user and returns the user
    """
    user = User.objects.create_user(
        username=data['username'], email=data['email'], password=data['password']
    )
    user.save()
    return user

def get_user(email):
    """
    this function returns a specific user by using the email of the user
    """
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        raise serializers.ValidationError('No user associated with this email.')