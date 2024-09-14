"""
URL configuration for Developer_Akademie_Join_Backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todolist.views import ContactsView, LoginView, RegisterView, TodoItemView
from todolist.functions import get_csrf_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/csrf-token/', get_csrf_token, name='csrf-token'),
    path('api/tasks/', TodoItemView.as_view(), name='tasks'),
    path('api/tasks/<int:task_id>/', TodoItemView.as_view(), name='task-detail'),
    path('api/contacts/', ContactsView.as_view(), name='contacts'),
    path('api/contacts/<int:contact_id>/', ContactsView.as_view(), name='contact-detail')
]
