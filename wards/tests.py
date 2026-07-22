from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from hospitals.models import Hospital
from .models import Ward


class WardModelTest(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            hospital_name="North District Clinic",
            location="Denver, CO",
            founded_year=1998
        )
        self.ward = Ward.objects.create(
            ward_name="Cardiology Wing A",
            capacity=45,
            hospital=self.hospital
        )

    def test_ward_creation(self):
        self.assertEqual(self.ward.ward_name, "Cardiology Wing A")
        self.assertEqual(self.ward.capacity, 45)
        self.assertEqual(self.ward.hospital, self.hospital)

    def test_capacity_validation(self):
        invalid_ward = Ward(
            ward_name="Invalid Ward",
            capacity=600,  # Exceeds max 500
            hospital=self.hospital
        )
        with self.assertRaises(ValidationError):
            invalid_ward.full_clean()


class WardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username="admin",
            email="admin@bphospitals.com",
            password="adminpassword123"
        )
        self.hospital = Hospital.objects.create(
            hospital_name="Riverside General",
            location="Austin, TX",
            founded_year=2005
        )
        self.ward = Ward.objects.create(
            ward_name="ICU Alpha",
            capacity=25,
            hospital=self.hospital
        )

    def test_ward_list_view(self):
        self.client.login(username="admin", password="adminpassword123")
        response = self.client.get(reverse('ward_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ICU Alpha")
