from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Hospital


class HospitalModelTest(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            hospital_name="St. Jude Medical Center",
            location="San Francisco, CA",
            founded_year=1985
        )

    def test_hospital_creation(self):
        self.assertEqual(self.hospital.hospital_name, "St. Jude Medical Center")
        self.assertEqual(self.hospital.location, "San Francisco, CA")
        self.assertEqual(self.hospital.founded_year, 1985)

    def test_unique_hospital_name_constraint(self):
        with self.assertRaises(Exception):
            Hospital.objects.create(
                hospital_name="St. Jude Medical Center",
                location="Los Angeles, CA",
                founded_year=2000
            )

    def test_founded_year_validation(self):
        invalid_hospital = Hospital(
            hospital_name="Future Hospital",
            location="Miami, FL",
            founded_year=1750  # Before 1800
        )
        with self.assertRaises(ValidationError):
            invalid_hospital.full_clean()


class HospitalViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username="admin",
            email="admin@bphospitals.com",
            password="adminpassword123"
        )
        self.hospital = Hospital.objects.create(
            hospital_name="Mercy General",
            location="Sacramento, CA",
            founded_year=1992
        )

    def test_unauthenticated_redirect(self):
        response = self.client.get(reverse('hospital_list'))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_hospital_list(self):
        self.client.login(username="admin", password="adminpassword123")
        response = self.client.get(reverse('hospital_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mercy General")

    def test_hospital_creation_view(self):
        self.client.login(username="admin", password="adminpassword123")
        response = self.client.post(reverse('hospital_create'), {
            'hospital_name': 'New Hope Hospital',
            'location': 'Seattle, WA',
            'founded_year': 2010
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Hospital.objects.filter(hospital_name='New Hope Hospital').exists())
