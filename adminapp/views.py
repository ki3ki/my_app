from rest_framework import viewsets, permissions, status, exceptions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render, get_object_or_404, redirect
from userapp.models import Task
from .models import App, AppCategory, AppSubCategory
from .serializers import (
    AppSerializer, 
    AppCategorySerializer, 
    CustomTokenObtainPairSerializer,
    AppSubCategorySerializer, 
    TaskSerializer
)
from .permissions import IsAdminUser
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

class AdminTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Views for rendering admin pages (HTML templates)
def admin_login_view(request):
    return render(request, 'adminapp/admin_login.html')

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def admin_dashboard_view(request):
    return render(request, 'adminapp/admin_dashboard.html')

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def admin_categories_view(request):
    return render(request, 'adminapp/categories.html')

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def admin_subcategories_view(request):
    return render(request, 'adminapp/subcategories.html')

def admin_add_apps_view(request):
    return render(request, 'adminapp/admin_add_apps.html')

def admin_task_list_view(request):
    return render(request, 'adminapp/admin_task.html')

def admin_user_list_view(request):
    return render(request, 'adminapp/admin_user.html')

def admin_app_detail_view(request, app_id):
    app = get_object_or_404(App, id=app_id)
    return render(request, 'adminapp/admin_app_details.html', {'app': app})

# ViewSets for CRUD operations
class AppCategoryViewSet(viewsets.ModelViewSet):
    queryset = AppCategory.objects.all()
    serializer_class = AppCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AppSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = AppSubCategory.objects.all()
    serializer_class = AppSubCategorySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request, *args, **kwargs):
        try:
            category_id = request.query_params.get('category')
            queryset = self.get_queryset()
            
            if category_id:
                queryset = queryset.filter(category_id=category_id)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, *args, **kwargs):
        try:
            # Validate that category exists
            category_id = request.data.get('category')
            if not category_id:
                return Response({
                    'error': 'Category ID is required'
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                AppCategory.objects.get(id=category_id)
            except AppCategory.DoesNotExist:
                return Response({
                    'error': 'Invalid category ID'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            # Validate category if it's being updated
            category_id = request.data.get('category')
            if category_id:
                try:
                    AppCategory.objects.get(id=category_id)
                except AppCategory.DoesNotExist:
                    return Response({
                        'error': 'Invalid category ID'
                    }, status=status.HTTP_400_BAD_REQUEST)

            serializer = self.get_serializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            # Check if subcategory is being used by any apps
            if instance.app_set.exists():
                return Response({
                    'error': 'Cannot delete subcategory as it is being used by one or more apps'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request, *args, **kwargs):
        

        try:
            # Handle file upload
            logo = request.FILES.get('logo')
            
            # Prepare data
            data = {
                'name': request.data.get('name'),
                'description': request.data.get('description', 'No Description provided'),
                'points': request.data.get('points', 0),
                'download_link': request.data.get('download_link'),
                'category': request.data.get('category'),
                'subcategory': request.data.get('subcategory'),
            }

            if logo:
                data['logo'] = logo


            serializer = self.get_serializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            # Handle file upload
            logo = request.FILES.get('logo')
            
            # Prepare data
            data = {
                'name': request.data.get('name', instance.name),
                'description': request.data.get('description', instance.description),
                'points': request.data.get('points', instance.points),
                'download_link': request.data.get('download_link', instance.download_link),
                'category': request.data.get('category', instance.category_id),
                'subcategory': request.data.get('subcategory', instance.subcategory_id),
            }

            if logo:
                if instance.logo:
                    instance.logo.delete(save=False)
                data['logo'] = logo

            serializer = self.get_serializer(instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            if instance.logo:
                instance.logo.delete(save=False)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['POST'])
    def add_points(self, request, pk=None):
        try:
            app = self.get_object()
            points_to_add = request.data.get('points')
            
            try:
                points_to_add = int(points_to_add)
                if points_to_add < 0:
                    return Response({
                        'error': 'Points must be a positive number'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                app.points = points_to_add
                app.save()
                
                return Response({
                    'current_points': app.points
                })
            except ValueError:
                return Response({
                    'error': 'Invalid points value'
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['get', 'put'], permission_classes=[IsAdminUser])
    def manage_tasks(self, request, pk=None):
        app = self.get_object()
        tasks = app.task_set.all()
        
        if request.method == 'GET':
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        
        if request.method == 'PUT':
            task = get_object_or_404(tasks, id=request.data.get('task_id'))
            task.status = request.data.get('status', task.status)
            task.save()
            return Response({"message": "Task updated successfully!"})

class TaskViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def list(self, request):
        # Fetch all tasks with status 'Pending'
        tasks = Task.objects.filter(status='Pending')
        serializer = TaskSerializer(tasks, many=True)
        print(serializer)
        return Response(serializer.data)

    def update(self, request, pk=None):
        task = Task.objects.get(pk=pk)
        status = request.data.get('status')

        if status not in ['Completed', 'Rejected']:
            return Response({"error": "Invalid status value"}, status=status.HTTP_400_BAD_REQUEST)

        task.status = status
        task.save()

        if status == 'Completed':
            task.user.points += task.app.points
            task.user.save()
            task.description = "Tasks completed"
            task.save()
        if status == 'Rejected':
            task.description = "Screenshot Rejected"
            task.save()

        return Response({"message": "Task updated successfully!"})