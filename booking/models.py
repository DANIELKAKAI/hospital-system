import uuid

from django.db import models

from users.models import User


class Booking(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="doctor_bookings"
    )
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="patient_bookings"
    )
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        db_table = "booking"
        ordering = ["start_time"]
