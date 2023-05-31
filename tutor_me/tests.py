# from django.test import TestCase
#
# # Create your tests here.
# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth.models import User
#
#
# class LoginTestCase(TestCase):
#
#     # references to write test cases
#     # you have to create your test data globally to make it work, don't enter it seperately everytime,
#     # otherwise it will take time
#     # def test_login_page(self):
#     #     response = self.client.get('/login/')
#     #     self.assertEqual(response.status_code, 200)
#     #     self.assertContains(response, 'Welcome to TutorMe!')
#     #     self.assertContains(response, 'Login with Google')
#     #     self.assertContains(response, 'method="POST"')
#     #     self.assertContains(response, '{% csrf_token %}')
#     #     add
#
#     @classmethod
#     def setUpTestData(cls):
#         cls.user = User.objects.create_user(
#             username='testuser',
#             email='testuser@example.com',
#             password='testpassword'
#         )
#
#
#     def test_login_view(self):
#         # Test that the login view is accessible
#         self.client.force_login(self.user)
#         response = self.client.get(reverse('tutor_me:login'))
#         self.assertContains(response, 'Welcome to TutorMe!')
#
#     def test_login_success(self):
#         # Test that a user can successfully log in
#         response = self.client.post(reverse('tutor_me:login'),
#         {'username': 'testuser', 'password': 'testpassword'})
#         self.assertEqual(response.status_code, 200)
#
#     def test_login_failure(self):
#         # Test that an incorrect username or password results in a failed login attempt
#         response = self.client.post(reverse('tutor_me:login'),
#         {'username': 'testuser', 'password': 'wrongpassword'})
#         self.assertEqual(response.status_code, 200)

from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Course, Availability, Appointment, Rate
from datetime import datetime
from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse


class LoginTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )
    def test_group_assignment(self):
        self.client.login(username='testuser', password='testpassword')
        student_group = Group.objects.create(name='student')
        tutor_group = Group.objects.create(name='tutor')
        response = self.client.get(reverse('tutor_me:redirect'), {'group': student_group.id})
        self.assertFalse(self.user.groups.filter(name='tutor').exists())

    # def test_login_view(self):
    #     # Test that the login view is accessible
    #     self.client.force_login(self.user)
    #     response = self.client.get(reverse('tutor_me:login'))
    #     self.assertContains(response, 'Welcome to TutorMe')

    def test_login_success(self):
        # Test that a user can successfully log in
        response = self.client.post(reverse('tutor_me:login'),
        {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        # Test that an incorrect username or password results in a failed login attempt
        response = self.client.post(reverse('tutor_me:login'),
        {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, 200)
    
    def test_add_availability(self):
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('tutor_me:tutor'), {'start_time': datetime.now(), 'end_time': datetime.now()})
        self.assertEqual(response.status_code, 200)

    def test_submit_request_button(self):
        # Test that the submit_request button is clickable
        response = self.client.get(reverse('tutor_me:submit_request'))
        self.assertContains(response, 'input type="submit" '
                                      'value="Submit"')

    def  test_student_view(self):
        # Test that the student_view is accessible
        self.client.force_login(self.user)
        response = self.client.get(reverse('tutor_me:index'))
        self.assertEqual(response.status_code, 200)

    def test_submit_request(self):
        # Test that the submit_request form shows up
        self.client.force_login(self.user)
        response = self.client.get(reverse('tutor_me:submit_request'))
        self.assertContains(response, 'Tutor availability information:')


    def test_hourly_rate(self):
        response = self.client.post(reverse('tutor_me:tutor'),
                                    {'username': 'testuser', 'password': 'testpassword', 'rate': '10'})
        self.assertEqual(response.status_code, 200)


    # def test_fill_the_request_form(self):
    #
    #     self.client.force_login(self.user)
    #     url = reverse('tutor_me:submit_request')
    #     data = {
    #         'id': '1',
    #         'tutor': 'Isiah ',
    #         'course': 'Math',
    #         'date': '2023-04-16',
    #         'start': '09:00',
    #         'end': '10:00',
    #         'start_time': '2023-04-16T09:30',
    #         'end_time': '2023-04-16T10:30',
    #         'note': ' Homework',
    #     }
    #     response = self.client.post(url, data=data)
    #
    #     self.assertRedirects(response, 'tutor: success', status_code=302, target_status_code=200)