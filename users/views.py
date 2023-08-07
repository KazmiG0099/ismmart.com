# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from .models import CustomUser
# from .serializers import UserSerializer
# from .utils import send_otp_code
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# import random

# class UserRegistrationView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSerializer

#     def generate_otp(self):
#         return str(random.randint(100000, 999999))

#     def perform_create(self, serializer):
#         user = serializer.save()
#         otp_code = self.generate_otp()
#         send_otp_code(user.email, otp_code)

# class UserLoginView(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         user = authenticate(request, email=email, password=password)
#         print(user)
#         if user is None:
#             return Response({'error': 'Invalid credentials'}, status=400)

#         # Log the user in using session-based authentication
#         login(request, user)

#         return Response({'message': 'Login successful'})

# @method_decorator(login_required, name='dispatch')
# class UserLogoutView(APIView):
#     def post(self, request):
#         # Log the user out
#         request.user.logout()

#         return Response({'message': 'Logout successful'})

# -----------------------------------------------------------------------------------------

import random
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import UserSerializer

User = get_user_model()

class UserRegistrationView(APIView):
    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def send_welcome_email(self, email):
        subject = 'Welcome to Our App'
        message = 'Thank you for registering on our app!'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

    def send_otp_code(self, email, otp_code):
        subject = 'OTP Code for Registration'
        message = f'Your OTP Code is: {otp_code}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Check if the email is already registered
            if User.objects.filter(email=email).exists():
                return Response({'error': 'Email already registered'}, status=status.HTTP_409_CONFLICT)

            # Save the user object without creating a user yet
            user = serializer.save()

            # Send welcome email
            self.send_welcome_email(email)

            # Generate and save OTP code in the user model
            otp_code = self.generate_otp()
            user.otp_code = otp_code
            user.save()

            # Send OTP code to user's email
            self.send_otp_code(email, otp_code)

            return Response({'message': 'Registration successful. Please check your email for OTP verification.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OTPVerificationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')

        user = CustomUser.objects.filter(email=email).first()

        if user is None:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp_code != otp_code:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        # Clear the OTP code after successful verification
        user.otp_code = None
        user.save()

        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = CustomUser.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is verified (OTP code is None)
        if user.otp_code is not None:
            return Response({'error': 'User not verified'}, status=status.HTTP_401_UNAUTHORIZED)

        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

class UserLogoutView(APIView):
    def post(self, request):
        # Log the user out
        request.user.logout()

        return Response({'message': 'Logout successful'})
