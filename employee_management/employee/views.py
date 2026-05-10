from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer, FormSerializer, EmployeeSerializer, UserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Form, Employee
import random
import string
from django.contrib.auth import logout


# In-memory token store for demo
RESET_TOKENS = {}



class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {'message': 'Registration successful','access': str(refresh.access_token),'refresh': str(refresh)}, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({'message': 'Login successful', 'access': str(refresh.access_token),'refresh': str(refresh)}, status=status.HTTP_200_OK)
    


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    
    
# ============================== Form Views ==============================

 
class FormAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        print("=====================================================", request.user)
        user = User.objects.get(id=request.user.id)
        forms = Form.objects.filter(created_by=user)
        serializer = FormSerializer(forms,many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FormSerializer(data=request.data)
        print("=====================================================", serializer)

        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            serializer.save(created_by=user)
            # user = User.objects.get(id=1)
            print("==========================user===========================", user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class FormDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        form = Form.objects.get(id=pk)
        serializer = FormSerializer(form,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        form = Form.objects.get(id=pk)
        form.delete()
        return Response({'message': 'Form deleted'})


class EmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        search = request.GET.get('search')
        employees = Employee.objects.all()
        if search:
            employees = employees.filter(data__icontains=search)
        serializer = EmployeeSerializer(employees,many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            # user = User.objects.get(id=1)
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# ============================== Employee Detail Views ==============================

class EmployeeDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]

    def put(self, request, pk):
        employee = Employee.objects.get(id=pk)
        serializer = EmployeeSerializer(employee,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = Employee.objects.get(id=pk)
        employee.delete()
        return Response({'message': 'Employee deleted'})
    
# from django.shortcuts import get_object_or_404

# class EmployeeDetailAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     def put(self, request, pk):
#         employee = get_object_or_404(Employee, id=pk)
#         serializer = EmployeeSerializer(employee, data=request.data, partial=True)

#         if serializer.is_valid():
#             employee = serializer.save()

#             user = employee.user
#             if user:
#                 user_data = request.data.get("data", {})

#                 username = user_data.get("User Name")
#                 email = user_data.get("email")

#                 if username:
#                     # prevent duplicates
#                     if User.objects.exclude(id=user.id).filter(username=username).exists():
#                         return Response({"error": "Username already exists"}, status=400)
#                     user.username = username

#                 if email:
#                     user.email = email

#                 user.save()

#             return Response(serializer.data)

#         return Response(serializer.errors, status=400)

#     def delete(self, request, pk):
#         employee = Employee.objects.get(id=pk)
#         employee.delete()
#         return Response({'message': 'Employee deleted'})


       


# ==========================  Password Reset API ==========================
class PasswordResetAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successful.'})
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        


class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})