from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from booking.models import Booking
from booking.serializers import BookingSerializer


class BookingView(APIView):
    serializer_class = BookingSerializer
    queryset = Booking.objects.select_related("doctor", "patient")
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.user.role != "patient":
            return Response(
                {"detail": "Only patient can create booking"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.serializer_class(
            data=request.data, context={"patient_id": request.user.id}
        )
        if serializer.is_valid(raise_exception=True):
            booking = serializer.save()
            serializer = self.serializer_class(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        bookings = self.queryset.filter(
            Q(doctor=request.user) | Q(patient=request.user)
        )
        serializer = self.serializer_class(bookings, many=True)
        return Response(serializer.data)
