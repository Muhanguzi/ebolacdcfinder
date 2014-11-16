from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from user_profile.models import UserProfile
from django.contrib.auth.models import User

class UserProfileDefaultPageTest(TestCase):
	fixtures = ['user_profiles.json', 'users.json']
		
	def test_user_profile_page(self):
		profile = UserProfile.objects.all()[0]
		response = self.client.get('/user-account/profile/%s/' % profile.user.username)
		self.assertEqual(response.status_code, 200)



class UserProfileUpdatePageTest(TestCase):
	fixtures = ['user_profiles.json', 'users.json']

	def setUp(self):
		self.client = Client()
		user = User.objects.create_user(username='test_user', 
			password='test', email='ivan.pasic@hotmail.com')
		user_profile = UserProfile.objects.create(user=user)

	# Test 'update profile' page when user is not logged in
	def test_user_profile_update_page_when_not_logged_in(self):
		profile = UserProfile.objects.all()[0]
		response = self.client.get('/user-account/profile/%s/update_profile/' % profile.user.username)
		self.assertRedirects(response, 
			'/user-account/login/?next=/user-account/profile/%s/update_profile/' % profile.user.username)

	# Test 'update profile' page when user is logged in
	def test_user_profile_update_page_when_logged_in(self):
		login = self.client.login(username='test_user', password='test') 
		self.assertTrue(login) 

		# Test that logged in user can access his page for profile updating
		profile=UserProfile.objects.get(user__username='test_user')
		response = self.client.get('/user-account/profile/%s/update_profile/' % profile.user.username)
		self.assertEqual(response.status_code, 200)

		# Test that logged in user can't access update profile page of some other user
		profile = UserProfile.objects.all()[0]
		response = self.client.get('/user-account/profile/%s/update_profile/' % profile.user.username)
		self.assertEqual(response.status_code, 403)



class UserProfileSettingsPageTest(TestCase):
	fixtures = ['user_profiles.json', 'users.json']

	def setUp(self):
		self.client = Client()
		user = User.objects.create_user(username='test_user', 
			password='test', email='ivan.pasic@hotmail.com')
		user_profile = UserProfile.objects.create(user=user)

	# Test settings page when user is not logged in
	def test_user_profile_settings_page_when_not_logged_in(self):
		profile = UserProfile.objects.all()[0]
		response = self.client.get('/user-account/profile/%s/settings/' % profile.user.username)
		self.assertRedirects(response, 
			'/user-account/login/?next=/user-account/profile/%s/settings/' % profile.user.username)
	
	# Test settings page when user is logged in	
	def test_user_profile_settings_page_when_logged_in(self):
		login = self.client.login(username='test_user', password='test') 
		self.assertTrue(login) 

		# Test that logged in user can access his settings page
		profile=UserProfile.objects.get(user__username='test_user')
		response = self.client.get('/user-account/profile/%s/settings/' % profile.user.username)
		self.assertEqual(response.status_code, 200)

		# Test that logged in user can't access settings page of some other user
		profile = UserProfile.objects.all()[0]
		response = self.client.get('/user-account/profile/%s/settings/' % profile.user.username)
		self.assertEqual(response.status_code, 403)


class DeleteUserProfileSettingsPageTest(TestCase):
	fixtures = ['user_profiles.json', 'users.json']

	def setUp(self):
		self.client = Client()
		user = User.objects.create_user(username='test_user', 
			password='test', email='ivan.pasic@hotmail.com')
		user_profile = UserProfile.objects.create(user=user)

	def test_deleting_of_an_account(self):
		login = self.client.login(username='test_user', password='test') 
		self.assertTrue(login) 

		# Test that logged in user can delete his account
		profile = UserProfile.objects.get(user__username='test_user')
		delete_url = "/user-account/user_account/profile/%s/delete-account/"  % profile.user.username
		response = self.client.post(delete_url, {"password": "test"})
		self.assertContains(response, "Your account has been deleted")

		# Test that logged in user can't delete some other user's account
		profile = UserProfile.objects.all()[0]
		response = self.client.get('/user-account/user_account/profile/%s/delete-account/' % profile.user.username)
		self.assertEqual(response.status_code, 403)