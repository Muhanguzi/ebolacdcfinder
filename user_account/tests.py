from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

class LoginTest(TestCase):
	def setUp(self):
		self.client = Client()
		user = User.objects.create_user(username='test_user', 
			password='test', email='ivan.pasic@hotmail.com')

	def test_response_for_get(self):
		response =  self.client.get('/user-account/login/')
		self.assertEqual(response.status_code, 200)
		
	def test_if_user_can_login(self):
		login = self.client.login(username='test_user', password='test') 
		self.assertTrue(login) 
       

class UserRegistrationTest(TestCase):
        def test_response_for_get(self):
            response = self.client.get("/user-account/create-account/")
            self.assertEqual(response.status_code, 200)

        def test_registration_form(self):            
            response = self.client.post("/user-account/create-account/", 
            	{"first_name": "Joe", "last_name": "Doe", "email": "ivan.pasic@hotmail.com", 
            	"username":"test_user", "password1":"test",	"password2":"test"})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response['Location'], 'http://testserver/user_account/account-successfully-created/')
            
            response = self.client.post("/user-account/create-account/", {})
            self.assertEqual(response.status_code, 200) 