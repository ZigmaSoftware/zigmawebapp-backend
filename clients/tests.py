from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase

from clients.models import Job


class AdminApiLoginTests(APITestCase):
    def setUp(self):
        self.login_url = reverse("admin-api-login")
        self.token_login_url = reverse("admin-api-token-login")
        self.jobs_url = reverse("job-list")
        self.contact_us_url = reverse("contactus-list")
        user_model = get_user_model()

        self.staff_user = user_model.objects.create_user(
            username="admin",
            password="admin@123",
            is_staff=True,
        )
        self.super_user = user_model.objects.create_superuser(
            username="superadmin",
            email="superadmin@example.com",
            password="super@123",
        )
        self.non_staff_user = user_model.objects.create_user(
            username="regular",
            password="regular@123",
            is_staff=False,
        )

    def test_staff_user_can_login_with_json_without_csrf_token(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.post(
            self.login_url,
            {"username": "admin", "password": "admin@123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.staff_user.username)
        self.assertIn("sessionid", response.cookies)

    def test_invalid_credentials_return_401(self):
        response = self.client.post(
            self.login_url,
            {"username": "admin", "password": "wrong-password"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_non_staff_user_is_rejected(self):
        response = self.client.post(
            self.login_url,
            {"username": "regular", "password": "regular@123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_missing_fields_return_400(self):
        response = self.client.post(
            self.login_url,
            {"username": "admin"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_staff_user_gets_token(self):
        response = self.client.post(
            self.token_login_url,
            {"username": "admin", "password": "admin@123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertEqual(response.data["token_type"], "Token")
        self.assertIn("token_created_at", response.data)
        self.assertIn("token_expires_at", response.data)
        self.assertIn("server_time", response.data)
        self.assertIn("token_age_seconds", response.data)
        self.assertIn("expires_in_seconds", response.data)
        self.assertGreaterEqual(response.data["expires_in_seconds"], 7190)
        self.assertLessEqual(response.data["expires_in_seconds"], 7200)

    def test_super_admin_gets_token(self):
        response = self.client.post(
            self.token_login_url,
            {"username": "superadmin", "password": "super@123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    def test_non_staff_cannot_get_token(self):
        response = self.client.post(
            self.token_login_url,
            {"username": "regular", "password": "regular@123"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_job_requires_auth(self):
        payload = {
            "title": "Backend Developer",
            "department": "Engineering",
            "location": ["Bengaluru"],
            "job_type": "Full Time",
            "experience_required": "2+ years",
            "qualifications": ["Python", "Django"],
            "responsibilities": ["Build APIs", "Write tests"],
        }

        response = self.client.post(self.jobs_url, payload, format="json")
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])

    def test_create_job_with_admin_token_succeeds(self):
        token_response = self.client.post(
            self.token_login_url,
            {"username": "admin", "password": "admin@123"},
            format="json",
        )
        token = token_response.data["access_token"]

        auth_client = APIClient()
        auth_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        payload = {
            "title": "Backend Developer",
            "department": "Engineering",
            "location": ["Bengaluru"],
            "job_type": "Full Time",
            "experience_required": "2+ years",
            "qualifications": ["Python", "Django"],
            "responsibilities": ["Build APIs", "Write tests"],
        }

        response = auth_client.post(self.jobs_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)

    def test_create_job_with_super_admin_token_succeeds(self):
        token_response = self.client.post(
            self.token_login_url,
            {"username": "superadmin", "password": "super@123"},
            format="json",
        )
        token = token_response.data["access_token"]

        auth_client = APIClient()
        auth_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")

        payload = {
            "title": "Data Engineer",
            "department": "Engineering",
            "location": ["Pune"],
            "job_type": "Full Time",
            "experience_required": "3+ years",
            "qualifications": ["Python", "SQL"],
            "responsibilities": ["Build pipelines", "Manage ETL"],
        }

        response = auth_client.post(self.jobs_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Job.objects.count(), 1)

    def test_create_job_with_non_admin_token_fails(self):
        token = Token.objects.create(user=self.non_staff_user)

        auth_client = APIClient()
        auth_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        payload = {
            "title": "QA Engineer",
            "department": "Engineering",
            "location": ["Hyderabad"],
            "job_type": "Full Time",
            "experience_required": "1+ years",
            "qualifications": ["Testing"],
            "responsibilities": ["Write test cases"],
        }

        response = auth_client.post(self.jobs_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_expired_token_fails_after_two_hours(self):
        token = Token.objects.create(user=self.staff_user)
        Token.objects.filter(pk=token.pk).update(
            created=timezone.now() - timedelta(hours=3)
        )
        expired_token = Token.objects.get(pk=token.pk)

        auth_client = APIClient()
        auth_client.credentials(HTTP_AUTHORIZATION=f"Token {expired_token.key}")

        payload = {
            "title": "Platform Engineer",
            "department": "Engineering",
            "location": ["Remote"],
            "job_type": "Full Time",
            "experience_required": "4+ years",
            "qualifications": ["Python", "DevOps"],
            "responsibilities": ["Own deployment pipeline"],
        }

        response = auth_client.post(self.jobs_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(str(response.data["detail"]), "Token has expired. Please login again.")

    def test_contact_us_create_succeeds_without_auth(self):
        payload = {
            "name": "Sameer Kumar",
            "email": "sameer@example.com",
            "phone": "9876543210",
            "category": "general_inquiry",
            "message": "I need support for the careers page integration.",
        }

        response = self.client.post(self.contact_us_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], payload["name"])

    def test_contact_us_short_message_fails_validation(self):
        payload = {
            "name": "Sameer Kumar",
            "email": "sameer@example.com",
            "phone": "9876543210",
            "category": "general_inquiry",
            "message": "Too short",
        }

        response = self.client.post(self.contact_us_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
