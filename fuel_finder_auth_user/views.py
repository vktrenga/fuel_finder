from urllib import response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserProfileSerializer, UserRegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from fuel_finder_auth_user.models import UserProfile
from rest_framework import status
from rest_framework.response import Response
#  Registration view
class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


# JWT Login view
class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims if needed
        token['username'] = user.username
        return token

class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]  # JWT Auth
    permission_classes = [IsAuthenticated]        # Only authenticated users

    def get(self, request):
        """Return the profile of the logged-in user"""
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Update or create user profile"""
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
