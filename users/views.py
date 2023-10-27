from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.serializers import SignUpSerializer, SignUpDoctorSerializer


class SignUpDoctorView(APIView):
    def post(self, request):
        serializer = SignUpDoctorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            serializer = SignUpDoctorSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class SignUpPatientView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.user.role != "doctor":
            return Response(
                {"detail": "Only a doctor can sign up a patient"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            serializer = SignUpSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
