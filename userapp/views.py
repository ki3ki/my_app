from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser, UserProfile, Task
from .serializers import CustomUserSerializer, TaskSerializer, UserProfileSerializer, UserPointsSerializer
from rest_framework import status
from django.shortcuts import render, get_object_or_404
from adminapp.models import App
from rest_framework.status import HTTP_200_OK
from adminapp.serializers import AppSerializer
from rest_framework import generics
from django.utils import timezone

def index_view(request):
    return render(request, 'index.html')


# Render the login page
def login_view(request):
    return render(request, 'userapp/login.html')

# Render the registration page
def register_view(request):
    return render(request, 'userapp/register.html')

# Render the user points list page
def dashboard_view(request):
    return render(request, 'userapp/dashboard.html', {'username': None})

# Render task completion page
def task_completion_view(request):
    app_id = request.GET.get('app_id')
    return render(request, 'userapp/task_completion.html', {'app_id': app_id})

# Render the user profile page
def profile_view(request):
    return render(request, 'userapp/profile.html')

# Render the user points list page
def user_points_list_view(request):
    return render(request, 'userapp/user_points_list.html', {'username': None})

# Render the user task list page
def user_task_list_view(request):
    return render(request, 'userapp/user_task_list.html', {'username': None})

# API view for fetching user points
class UserPointsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserPointsSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# API view for user registration and token generation
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        data['is_admin'] = data.get('is_admin', False)  # Default to regular user
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

            # Create a JWT token for the newly registered user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                "message": "User created and logged in successfully!",
                "access_token": access_token,
                "refresh_token": str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view for handling tasks (list and update task status)

class TaskCompletionView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)

        # Sort tasks by status: 'Completed', 'Pending', 'Rejected'
        completed_tasks = tasks.filter(status='Completed')
        pending_tasks = tasks.filter(status='Pending')
        rejected_tasks = tasks.filter(status='Rejected')

        # Serialize tasks
        completed_serializer = TaskSerializer(completed_tasks, many=True)
        pending_serializer = TaskSerializer(pending_tasks, many=True)
        rejected_serializer = TaskSerializer(rejected_tasks, many=True)


        return Response({
            'completed_tasks': completed_serializer.data,
            'pending_tasks': pending_serializer.data,
            'rejected_tasks': rejected_serializer.data
        })

    def post(self, request):
        # Get the data from the request
        app_id = request.data.get('app_id')
        screenshot = request.data.get('screenshot')

        # Ensure the screenshot is provided
        if not screenshot:
            return Response({"error": "Screenshot is required to complete the task."}, status=status.HTTP_400_BAD_REQUEST)

        #Check if the task already exists for the given user and app
        task, created = Task.objects.get_or_create(
            user=request.user, app_id=app_id,
            defaults={'status': 'Pending'}  # Create the task if it doesn't exist with status "Pending"
        )

        # If a new task is created, save the screenshot
        if created:
            task.screenshot = screenshot
            task.status = 'Pending'
            task.description = 'Submitted for Review '  # Set the task status to "Submitted for Review"
            task.save()

            # Return success response with the newly created task details
            return Response({
                "message": "Task created and screenshot uploaded successfully for review.",
                "task_id": task.id  # Optionally return the task ID of the created task
            }, status=status.HTTP_201_CREATED)

        # If the task already exists, just update the screenshot and the status
        task.screenshot = screenshot
        task.status = 'Submitted for Review'
        task.save()

        return Response({
            "message": "Screenshot uploaded successfully for review on the existing task.",
            "task_id": task.id  # Optionally return the task ID of the existing task
        }, status=status.HTTP_200_OK)


class AppDetailView(generics.RetrieveAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer

# API view for fetching and updating user profile
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view for fetching available apps
class AvailableAppsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        apps = App.objects.all()
        apps_data = [
            {
                'id': app.id,
                'name': app.name,
                'icon_url': app.logo.url if app.logo else '',
                'points': app.points
            }
            for app in apps
        ]
        return Response({'apps': apps_data}, status=status.HTTP_200_OK)

# API view for logging out by blacklisting the refresh token
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
                return Response({"detail": "Successfully logged out."}, status=HTTP_200_OK)
            return Response({"detail": "Refresh token is missing."}, status=400)
        except Exception as e:
            return Response({"detail": str(e)}, status=400)
