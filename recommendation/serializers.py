from .models import User
from rest_framework import serializers



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type' : 'password'},write_only=True)
    class Meta:
        model = User
        fields = ['fname', 'lname', 'email','phone','city','password']

    def save(self):
        user = User(
            fname=self.validated_data['fname'],
            lname=self.validated_data['lname'],
            email=self.validated_data['email'],
            phone=self.validated_data['phone'],
            city=self.validated_data['city'],

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

class RecommendSerializer(serializers.Serializer):
    experience = serializers.IntegerField(max_value=100, min_value=0)
    fee = serializers.IntegerField(min_value=0)
    city_name = serializers.CharField(style={"input_type": "text"},write_only=True)


class UserDetailsSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id','fname', 'lname','email','phone','city']


class EditDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['fname', 'lname','phone','city']

    def update(self, instance, validated_data):
        instance.fname = validated_data['fname']
        instance.lname = validated_data.get('lname', instance.lname)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.city = validated_data.get('city', instance.city)
        instance.save()
        print(instance.phone)
        return instance