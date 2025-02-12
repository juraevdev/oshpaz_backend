from rest_framework import generics, status, permissions
from accounts.serializers import *
from accounts.models import User, UserConfirmation
from rest_framework.response import Response
import logging
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.utils import timezone
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
    

class FollowUserApiView(generics.GenericAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        following_user = get_object_or_404(User, id=kwargs['user_id'])


        if request.user == following_user:
            return Response({'error': 'You cannot follow yourself!'}, status=status.HTTP_400_BAD_REQUEST)
        
        follow, created = Follow.objects.get_or_create(follow=request.user, following=following_user)

        return Response({'message': f"Your are now following {following_user.fullname}"}, status=status.HTTP_201_CREATED)
    

class UnfollowUserApiView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        following_user = get_object_or_404(User, id=kwargs['user_id'])
        follow = Follow.objects.filter(follow=request.user, following=following_user)

        follow.delete()
        return Response({'message': f"You have unfollowed {following_user.fullname}"}, status=status.HTTP_204_NO_CONTENT)
    

class FollowersListApiView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self):
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        return User.objects.filter(following__following=user)
    

class FollowingListApiView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def get(self):
        user = get_object_or_404(User, id=self.kwargs['user_id'])
        return User.objects.filter(follower_follower = user)
    
class BlockUserApiView(generics.GenericAPIView):
    serializer_class = BlocklistSerializer

    def post(self, request, *args, **kwargs):
        blocked_user = get_object_or_404(User, id=kwargs['user_id'])

        if request.user == blocked_user:
            return Response({'error': 'You cannot block yourself!'}, status=status.HTTP_400_BAD_REQUEST)
        
        block, created = Blocklist.objects.get_or_create(block=request.user, blocked_user=blocked_user)

        return Response({'message': f'You are now blocked {blocked_user.fullname}'}, status=status.HTTP_201_CREATED)
    
class UnblockUserApiView(generics.GenericAPIView):

    def delete(self, request, *args, **kwargs):
        blocked_user = get_object_or_404(User, id=kwargs['user_id'])
        block = Blocklist.objects.filter(blocker=request.user, blocked_user=blocked_user)

        if not block.exists():
            return Response({'error': 'This user is not blocked'}, status=status.HTTP_400_BAD_REQUEST)
        
        block.delete()
        return Response({'message': f'You have unblocked {blocked_user.get_full_name()}'}, status=status.HTTP_204_NO_CONTENT)
    

class BlockListApiView(generics.GenericAPIView):
    serializer_class = BlocklistSerializer

    def get_queryset(self):
        return Blocklist.objects.filter(blocker=self.request.user)
    

class PasswordResetRequestApiView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer


    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.data['phone_number']
            user = User.objects.filter(phone_number=phone_number).first()
            if user is None:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            code = user.generate_verify_code()
            return Response({'message': 'Code is sent to your phone number', 'code': code})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerifyApiView(generics.GenericAPIView):
    serializer_class = PasswordResetVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = serializer.data['code']
            user = request.user
            otp_code = UserConfirmation.objects.filter(code=code).first()
            if user is None:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            if otp_code is None or otp_code.expires < timezone.now():
                return Response({'message': 'Incorrect verification code'}, status=status.HTTP_400_BAD_REQUEST)
            otp_code.is_used = True
            otp_code.save()
            return Response({'message': 'Verification code is correct. Now you can change your password'}, status=status.HTTP_200_OK)
        return Response(serializer.errors)
    

class PasswordResetApiView(generics.GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = serializer.data['phone_number']
            new_password = serializer.data['new_password']
            confirm_password = serializer.data['confirm_password']
            user = User.objects.filter(phone_number=phone_number).first()
            otp_code = UserConfirmation.objects.filter(user=user, is_used=True).first()
            if user is None:
                return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            if otp_code is None:
                return Response({'message': 'Verification code not confirmed'}, status=status.HTTP_404_NOT_FOUND)
            if not otp_code.is_used:
                return Response({'message': 'Verification code not confirmed in this phone number'}, status=status.HTTP_401_UNAUTHORIZED)
            user.set_password(confirm_password)
            user.save()
            return Response({'message': 'Your password changed successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors)
    