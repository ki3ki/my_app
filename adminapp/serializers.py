from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import App, AppCategory, AppSubCategory
from userapp.models import Task
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['is_admin'] = bool(self.user.is_admin)  # Add custom claim for is_admin
        return data

# Serializer for AppCategory model
class AppCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppCategory  # Serialize all fields of the AppCategory model
        fields = '__all__'

# Serializer for AppSubCategory model
class AppSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AppSubCategory  # Serialize all fields of the AppSubCategory model
        fields = '__all__'

# Serializer for App model, includes nested category and subcategory
class AppSerializer(serializers.ModelSerializer):

    class Meta:
        model = App
        fields = ['id', 'name', 'description', 'points', 'category', 'subcategory', 'logo', 'download_link']
        read_only_fields = ['created_at', 'updated_at']

    def validate(self, data):
        # Validate category and subcategory relationship
        category = data.get('category')
        subcategory = data.get('subcategory')
        
        if subcategory and category and subcategory.category_id != category.id:
            raise serializers.ValidationError({
                "subcategory": "Selected subcategory does not belong to the selected category"
            })
        
        # Validate download link format
        download_link = data.get('download_link')
        if download_link:
            try:
                URLValidator()(download_link)
            except ValidationError:
                raise serializers.ValidationError({
                    "download_link": "Please enter a valid URL"
                })
        
        return data


# Serializer for updating the points of an app 
class AppUpdatePointsSerializer(serializers.ModelSerializer):
    points = serializers.IntegerField()  # Only allow updating the 'points' field

    class Meta:
        model = App  # Serialize the points field of the App model
        fields = ['points']  # Only allowing points update

# Serializer for Task model 
class TaskSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    app_name = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'username', 'app_name', 'screenshot', 'completed_at', 'status', 'description']

    def get_username(self, obj):
        return obj.user.username  # Fetch the username from the user field

    def get_app_name(self, obj):
        return obj.app.name  # Fetch the app name from the app field

    def validate_status(self, value):
        if value not in ['Pending', 'Completed', 'Rejected']:
            raise serializers.ValidationError("Invalid status value.")
        return value
