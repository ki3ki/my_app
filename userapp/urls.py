# userapp/urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


urlpatterns = [
    # Frontend Views
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('points/', views.user_points_list_view, name='user_points_list'),
    path('task/', views.task_completion_view, name='task-completion'),  # Task completion page
    path('profile/', views.profile_view, name='profile'),
    path('task/list/', views.user_task_list_view, name ='user_task_list'),

    # API Endpoints
    path('api/register/', views.RegisterView.as_view(), name='api_register'),
    path('api/login/', TokenObtainPairView.as_view(), name='api_token_obtain_pair'),
    path('api/auth/token/logout/', views.LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
    path('api/task/completion/', views.TaskCompletionView.as_view(), name='tasks'),  # API for task completion
    path('api/profile/', views.UserProfileView.as_view(), name='user_profile'),
    path('api/points/', views.UserPointsAPI.as_view(), name='api_user_points'),
    path('api/apps/', views.AvailableAppsView.as_view(), name='available_apps'),
    path('api/apps/<int:pk>/', views.AppDetailView.as_view(), name='app-detail'),
]