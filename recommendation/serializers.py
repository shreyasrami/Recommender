from .models import User
from rest_framework import serializers



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type' : 'password'},write_only=True)
    class Meta:
        model = User
        fields = ['fname', 'lname', 'email', 'password']

    def save(self):
        user = User(
            fname=self.validated_data['fname'],
            lname=self.validated_data['lname'],
            email=self.validated_data['email']

        )
        password = self.validated_data['password']
        user.set_password(password)
        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50)
    password = serializers.CharField(style={"input_type": "password"},write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']