from rest_framework import generics, status, permissions
from accounts.serializers import *
from accounts.models import User
from rest_framework.response import Response
import logging
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
logger = logging.getLogger(__name__)

class OshpazRegisterApiView(generics.GenericAPIView):
    serializer_class = OshpazRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['user_role'] = 'oshpaz'
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OshpazLoginApiView(generics.GenericAPIView):
    serializer_class = OshpazLoginSerializer    

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.validated_data['user_role'] = 'oshpaz'
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']

            oshpaz = User.objects.filter(phone_number=phone_number).first()
            if oshpaz is None:
                logger.warning(f"Login failed: User not found for phone number {phone_number}")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            if not oshpaz.check_password(password):
                logger.warning(f"Login failed: Incorrect password for phone number {phone_number}")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            logger.info(f"Login successful for phone number {phone_number}")
            refresh = RefreshToken.for_user(oshpaz)


            if serializer.validated_data.get('remember_me', False):
                refresh.set_exp(lifetime=timedelta(days=7))  

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class OshpazProfileApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OshpazProfileSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        data['user_role'] = 'oshpaz'
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OshpazProfileDetailApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OshpazProfileSerializer

    def get(self, request, id):
        data = request.data
        data['user_role'] = 'oshpaz'
        oshpaz = User.objects.get(id=id)
        serializer = self.get_serializer(oshpaz)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        try:
            refresh = request.data['refresh']
            token = RefreshToken(refresh)
            token.blacklist()
            return Response({'message': 'Logged out successfully!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Failed to logout'}, status=status.HTTP_400_BAD_REQUEST)
        

class UserRegisterApiView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['user_role'] = 'foydalanuvchi'
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginApiView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data['user_role'] = 'foydalanuvchi'
        if serializer.is_valid(raise_exception=True):
            phone_number = validated_data['phone_number']
            password = validated_data['password']
            user = User.objects.filter(phone_number=phone_number).first()
            if user is None:
                logger.warning(f"Login failed: User not found for phone number {phone_number}")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            if not user.check_password(password):
                logger.warning(f"Login failed: Incorrect password for phone number {phone_number}")
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            logger.info(f"Login successful for phone number {phone_number}")
            refresh = RefreshToken.for_user(oshpaz)

            if serializer.validated_data.get('remember_me', False):
                refresh.set_exp(lifetime=timedelta(days=7))  

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileApiView(generics.GenericAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        data['user_role'] = 'foydalanuvchi'
        serializer = self.get_serializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileDetailApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, id):
        data = request.data
        data['user_role'] = 'foydalanuvchi'
        user = User.objects.get(id=id)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)