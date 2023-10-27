from django.db.models import Q
from rest_framework import serializers

from booking.models import Booking
from users.serializers import UserSerializer


class BookingSerializer(serializers.Serializer):
    doctor = UserSerializer(read_only=True)
    doctor_id = serializers.UUIDField(write_only=True)
    patient = UserSerializer(read_only=True)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()

    def create(self, validated_data):
        validated_data["patient_id"] = self.context.get("patient_id")
        instance = Booking(**validated_data)
        instance.save()
        return instance

    def validate(self, validated_data):
        doctor_id = validated_data["doctor_id"]
        start_time = validated_data["start_time"]
        end_time = validated_data["end_time"]
        booking = (
            Booking.objects.filter(doctor_id=doctor_id)
            .filter(Q(start_time__gte=start_time) & Q(end_time__lte=end_time))
            .first()
        )
        if booking:
            serializers.ValidationError("That time slot is booked")
        return validated_data

    class Meta:
        model = Booking
        fields = (
            "id",
            "doctor",
            "doctor_id",
            "patient",
            "start_time",
            "end_time",
        )
