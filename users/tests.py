from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class TestUserViews(APITestCase):
    def setUp(self):
        self.doctor_url = reverse("doctor")
        self.patient_url = reverse("patient")
        self.doctor = User.objects.create_user(
            full_name="Test Doc",
            email="testdoc@test.com",
            password="testpass",
            role="doctor",
        )
        self.doctor_access_token = RefreshToken.for_user(
            self.doctor
        ).access_token
        self.patient = User.objects.create_user(
            full_name="Test Patient",
            email="testpatient@test.com",
            password="testpass",
            role="patient",
        )
        self.patient_access_token = RefreshToken.for_user(
            self.patient
        ).access_token

    def test_successful_doctor_self_signup(self):
        data = {
            "email": "doc6@gmail.com",
            "full_name": "fname lname",
            "password": "password",
            "role": "doctor",
        }
        response = self.client.post(self.doctor_url, data, format="json")
        res_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["email"], res_data["email"])
        self.assertEqual(data["full_name"], res_data["full_name"])
        self.assertEqual(data["role"], res_data["role"])
        self.assertIn("id", res_data.keys())

    def test_successful_patient_signup_by_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.doctor_access_token}"
        )
        data = {
            "email": "patient@gmail.com",
            "full_name": "fname lname",
            "password": "password",
            "role": "patient",
        }
        response = self.client.post(self.patient_url, data, format="json")
        res_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["email"], res_data["email"])
        self.assertEqual(data["full_name"], res_data["full_name"])
        self.assertEqual(data["role"], res_data["role"])
        self.assertIn("id", res_data.keys())

    def test_failed_patient_self_signup(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.patient_access_token}"
        )
        data = {
            "email": "pp@gmail.com",
            "full_name": "fname lname",
            "password": "password",
            "role": "patient",
        }
        response = self.client.post(self.patient_url, data, format="json")
        res_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            "Only a doctor can sign up a patient", res_data["detail"]
        )
