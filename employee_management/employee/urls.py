from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import FormAPIView, FormAPIView, RegisterAPIView,LoginAPIView, EmployeeAPIView, EmployeeDetailAPIView, FormDetailAPIView, PasswordResetAPIView, ProfileAPIView, LogoutAPIView

urlpatterns = [
    path('register/',RegisterAPIView.as_view()),
    path('login/',LoginAPIView.as_view()),
    path('token/refresh/',TokenRefreshView.as_view()),
    path('forms/',FormAPIView.as_view()),
    path('forms/<int:pk>/',FormDetailAPIView.as_view()),
    path('employees/',EmployeeAPIView.as_view()),
    path('employees/<int:pk>/',EmployeeDetailAPIView.as_view()),
    path('password-reset/', PasswordResetAPIView.as_view(), name='password-reset'),
    path('profile/', ProfileAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),


]