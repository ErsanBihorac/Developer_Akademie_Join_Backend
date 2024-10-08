from django.test import TestCase, Client
from .models import Contact, TodoItem
from django.contrib.auth.models import User
from django.urls import reverse

class TestViews(TestCase):
    def setUp(self):
        """
        This function sets up all needed information that will be used for testing in the other tests
        """
        self.test_contact = Contact.objects.create( 
            name='testcontact',
            email='testcontact@mail.com',
            phone='123456789',
            first_letter='ut',
            color_id=1
        )
        self.client = Client()
        self.contacts_url = reverse('contacts')
        self.contact_detail_url = reverse('contact-detail', args=[self.test_contact.id])
        self.csrf_token_url = reverse('csrf-token')
        self.tasks_url = reverse('tasks')
        
    def test_contacts_view_get(self):
        """
        This functions tests if contact information are callable
        """
        response = self.client.get(self.contacts_url, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_contacts_view_post(self):
        """
        This function tests if contacts can be added
        """
        test_contact2 = {
            'name': 'testcontact2',
            'email': 'testcontact2@mail.com',
            'phone': '123456789',
            'firstLetter': 't',
            'colorId': 1
        }

        response = self.client.post(self.contacts_url, test_contact2, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Contact.objects.last().name, 'testcontact2')

    def test_contacts_view_put(self):
        """
        This function tests if a specific contact can be updated
        """
        updated_test_contact = {
            'name': 'updated testcontact',
            'email': 'testcontact@mail.com',
            'phone': '123456789',
            'first_letter': 'u',
            'color_id': 1
        }
                
        response = self.client.put(self.contact_detail_url, updated_test_contact, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.last().name, 'updated testcontact')
        self.assertEqual(Contact.objects.count(), 1)

    def test_contacts_view_delete(self):         
        """
        This function tests if a specific contact can be deleted
        """
        response = self.client.delete(self.contact_detail_url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Contact.objects.count(), 0)

    def test_todo_item_view_get(self):
        """
        This function tests if todo items are callable
        """
        response = self.client.get(self.tasks_url, content_type='application/json')
        self.assertEqual(response.status_code, 200)

class TestModels(TestCase):
    def setUp(self):
        """
        This function sets up all the information that will be used to for the other tests
        """
        self.user = User.objects.create_user(username='testuser', 
                                             password='password', 
                                             email='testuser@mail.com')

    def test_model_Contact(self):
        """
        This function tests if the Contact model is of the Contact instance after creating
        """
        contact = Contact.objects.create(
            name='testcontact',
            email='testcontact@mail.com',
            phone='123456789',
            first_letter='t',
        )

        self.assertEqual(str(contact), 'testcontact')
        self.assertTrue(isinstance(contact, Contact))

    def test_model_TodoItem(self):
        """
        This function tests if the TodoItem model is of the TodoItem instance after creating
        """
        todo_item = TodoItem.objects.create(
            title='test_todo',
            description='this is a test',
            due_date='2026-01-01',
        )
        todo_item.assigned_to.set([self.user])

        self.assertEqual(str(todo_item), 'test_todo')
        self.assertTrue(isinstance(todo_item, TodoItem))