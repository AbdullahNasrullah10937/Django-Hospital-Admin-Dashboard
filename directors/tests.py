from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from hospitals.models import Hospital
from .models import HospitalDirector


class DirectorModelTest(TestCase):
    def setUp(self):
        self.hospital = Hospital.objects.create(
            hospital_name="Central City Hospital",
            location="Chicago, IL",
            founded_year=1975
        )
        self.director = HospitalDirector.objects.create(
            director_name="Dr. Robert Chen",
            qualification="MD, MHA",
            hospital=self.hospital
        )

    def test_director_creation(self):
        self.assertEqual(self.director.director_name, "Dr. Robert Chen")
        self.assertEqual(self.director.qualification, "MD, MHA")
        self.assertEqual(self.director.hospital, self.hospital)

    def test_director_name_numeric_validation(self):
        invalid_director = HospitalDirector(
            director_name="123456",
            qualification="MD",
            hospital=self.hospital
        )
        with self.assertRaises(ValidationError):
            invalid_director.clean()

    def test_one_to_one_relationship(self):
        with self.assertRaises(Exception):
            HospitalDirector.objects.create(
                director_name="Dr. Second Director",
                qualification="PhD",
                hospital=self.hospital
            )


class DirectorViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username="admin",
            email="admin@bphospitals.com",
            password="adminpassword123"
        )
        self.hospital = Hospital.objects.create(
            hospital_name="Eastside Clinic",
            location="Miami, FL",
            founded_year=2000
        )
        self.director = HospitalDirector.objects.create(
            director_name="Dr. Sarah Jenkins",
            qualification="DO, MBA",
            hospital=self.hospital
        )

    def test_director_list_view(self):
        self.client.login(username="admin", password="adminpassword123")
        response = self.client.get(reverse('director_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dr. Sarah Jenkins")
