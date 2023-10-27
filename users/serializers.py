from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "full_name", "role")


def valid_password(password):
    return len(password) >= 8


class SignUpSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "password", "role")

    def create(self, validated_data):
        password = validated_data.get("password")

        if password and not valid_password(password):
            raise serializers.ValidationError(
                {
                    "password": [
                        "Minimum Password length should be 8 characters"
                    ]
                }
            )

        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.get("password")

        if password and not valid_password(password):
            raise serializers.ValidationError(
                {
                    "password": [
                        "Minimum Password length should be 8 characters"
                    ]
                }
            )
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class SignUpDoctorSerializer(SignUpSerializer):
    def validate(self, validated_data):
        role = validated_data["role"]
        if role != "doctor":
            raise serializers.ValidationError("Only a doctor can self signup")
        return validated_data
