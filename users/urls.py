from django.urls import path

from users.views import SignUpDoctorView, SignUpPatientView

urlpatterns = [
    path("doctor", SignUpDoctorView.as_view(), name="doctor"),
    path("patient", SignUpPatientView.as_view(), name="patient"),
]
