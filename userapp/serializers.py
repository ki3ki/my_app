# userapp/serializers.py
from rest_framework import serializers
from .models import CustomUser,  UserProfile, Task
from adminapp.models import App 

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password', 'is_admin']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'points_earned', 'profile_picture', 'bio', 'contact_number', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    app_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = '__all__'

    def get_app_name(self, obj):
        return obj.app.name  # Fetch the app name from the app field


class UserPointsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'points']  


