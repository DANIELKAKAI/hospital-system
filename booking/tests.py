from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from booking.models import Booking
from users.models import User


class TestBookingViews(APITestCase):
    def setUp(self):
        self.booking_url = reverse("booking")
        self.doctor = User.objects.create_user(
            full_name="Test Doc",
            email="testdoc@test.com",
            password="testpass",
            role="doctor",
        )
        self.doctor_access_token = RefreshToken.for_user(
            self.doctor
        ).access_token
        self.doctor2 = User.objects.create_user(
            full_name="Test Doc2",
            email="testdoc2@test.com",
            password="testpass",
            role="doctor",
        )
        self.doctor_access_token2 = RefreshToken.for_user(
            self.doctor2
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
        self.patient2 = User.objects.create_user(
            full_name="Test Patient2",
            email="testpatient2@test.com",
            password="testpass",
            role="patient",
        )
        self.patient_access_token2 = RefreshToken.for_user(
            self.patient2
        ).access_token
        self.booking = Booking.objects.create(
            patient=self.patient,
            doctor=self.doctor,
            start_time="2023-10-27T15:30:00Z",
            end_time="2023-10-27T17:30:00Z",
        )

    def test_successful_booking_creation_by_patient(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.patient_access_token}"
        )
        data = {
            "doctor_id": str(self.doctor.id),
            "start_time": "2023-10-27T18:30:00Z",
            "end_time": "2023-10-27T19:30:00Z",
        }
        response = self.client.post(self.booking_url, data, format="json")
        res_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data["doctor_id"], res_data["doctor"]["id"])
        self.assertEqual(data["start_time"], res_data["start_time"])
        self.assertEqual(data["end_time"], res_data["end_time"])
        self.assertEqual(str(self.patient.id), res_data["patient"]["id"])
        self.assertIn("id", res_data.keys())

    def test_failed_booking_creation_by_patient_if_doctor_already_booked(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.patient_access_token}"
        )
        data = {
            "doctor_id": str(self.doctor.id),
            "start_time": "2023-10-27T15:30:00Z",
            "end_time": "2023-10-27T17:30:00Z",
        }
        response = self.client.post(self.booking_url, data, format="json")
        res_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("That time slot is booked", res_data["non_field_errors"][0])

    def test_failed_booking_creation_by_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.doctor_access_token}"
        )
        data = {
            "doctor_id": str(self.doctor.id),
            "start_time": "2023-10-27T15:30:00Z",
            "end_time": "2023-10-27T17:30:00Z",
        }
        response = self.client.post(self.booking_url, data, format="json")
        res_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual("Only patient can create booking", res_data["detail"])

    def test_patient_can_only_view_their_bookings(self):
        # patient who created booking
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.patient_access_token}"
        )
        response = self.client.get(self.booking_url)
        res_data = response.json()
        booking_data = res_data[0]
        self.assertEqual(str(self.patient.id), booking_data["patient"]["id"])

        # other patient
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.patient_access_token2}"
        )
        response = self.client.get(self.booking_url)
        res_data = response.json()
        self.assertEqual(res_data, [])

    def test_doctor_can_only_view_their_bookings(self):
        # doctor related to booking
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.doctor_access_token}"
        )
        response = self.client.get(self.booking_url)
        res_data = response.json()
        booking_data = res_data[0]
        self.assertEqual(str(self.doctor.id), booking_data["doctor"]["id"])

        # other doctor
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.doctor_access_token2}"
        )
        response = self.client.get(self.booking_url)
        res_data = response.json()
        self.assertEqual(res_data, [])
