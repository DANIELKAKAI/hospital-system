from django.urls import path

from booking.views import BookingView

urlpatterns = [path("", BookingView.as_view(), name="booking")]
