from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Form, Employee


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'password'
        ]

    def validate_email(self, value):

        if User.objects.filter(
            email=value
        ).exists():

            raise serializers.ValidationError(
                'Email already exists'
            )

        return value

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data[
                'username'
            ],

            email=validated_data[
                'email'
            ],

            password=validated_data[
                'password'
            ]
        )

        return user


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, attrs):

        user = authenticate(
            username=attrs['username'],
            password=attrs['password']
        )

        if not user:

            raise serializers.ValidationError(
                'Invalid credentials'
            )

        attrs['user'] = user

        return attrs
    


class FormSerializer(serializers.ModelSerializer):

    class Meta:
        model = Form
        fields = '__all__'
        read_only_fields = ['created_by']


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = ['user', 'created_at']


    def create(self, validated_data):
        data = validated_data.get('data', {})
        username = data.get('User Name')
        email = data.get('email')
        user = None
        if username:
            user = User.objects.create(
                username=username,
                email=email,
            )

        employee = Employee.objects.create(
            **validated_data
        )

        return employee
    
    def update(self, instance, validated_data):
        data = validated_data.get('data', {})
        print("Data in serializer update:", data)  
        username = data.get('User Name')
        print("Username in serializer update:", username)  
        email = data.get('email')

        user = instance.user
        if user:
            if username:
                # prevent duplicates
                if User.objects.exclude(id=user.id).filter(username=username).exists():
                    raise serializers.ValidationError({"error": "Username already exists"})
                user.username = username

            if email:
                user.email = email

            user.save()

        return super().update(instance, validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
