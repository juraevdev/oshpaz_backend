from rest_framework import serializers
from accounts.models import User

class OshpazRegisterSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    remember_me = serializers.BooleanField(default=False)

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:    
            raise serializers.ValidationError("Password didn't match")
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            fullname = validated_data['fullname'],
            phone_number = validated_data['phone_number'],
            password = validated_data['password'],
        )
        return user
    
    def to_representation(self, instance):
        return {
            "id": instance.id,
            "first_name": instance.first_name,
            "last_name": instance.last_name,
            "phone_number": instance.phone_number,
    }



class OshpazLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

class OshpazProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    fullname = serializers.CharField()
    gender = serializers.CharField()
    email = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'id', 'phone_number', 'profile_image', 'fullname', 'gender',
            'birth_date', 'email', 'bio', 'certificate', 'work_places', 
            'work_place_now', 'achievements', 'facebook', 'linkedin', 'instagram', 'telegram'
        ]
        
        def get_username(self, obj):
            return f"{obj.first_name} {obj.last_name}"


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()



class UserRegisterSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    phone_number = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    remember_me = serializers.BooleanField()

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            raise serializers.ValidationError("Password didn't match")
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            fullname = validated_data['fullname'],
            phone_number = validated_data['phone_number'],
            password = validated_data['password'],
        )
        return user
    

class UserLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField()
    phone_number = serializers.CharField()
    gender = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'id', 'fullname', 'phone_number', 'profile_image', 'gender'
        ]