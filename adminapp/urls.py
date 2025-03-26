from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    AdminTokenObtainPairView, AppViewSet, AppCategoryViewSet, AppSubCategoryViewSet, TaskViewSet,
    admin_login_view, admin_dashboard_view, admin_categories_view, admin_add_apps_view,
    admin_subcategories_view, admin_app_detail_view, admin_task_list_view, admin_user_list_view
)

# Register the viewsets with the router
router = DefaultRouter()
router.register('apps', AppViewSet, basename='apps')
router.register('categories', AppCategoryViewSet, basename='categories')
router.register('subcategories', AppSubCategoryViewSet, basename='subcategories')
router.register('tasks', TaskViewSet, basename='task')

app_name = 'adminapp'

urlpatterns = [
    # API Endpoints
    path('api/', include(router.urls)),
    
    # JWT Authentication Endpoints
    path('admin-login/', AdminTokenObtainPairView.as_view(), name='admin-login'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Admin Dashboard Views
    path('login/', admin_login_view, name='admin-login-page'),
    path('dashboard/', admin_dashboard_view, name='admin_dashboard'),
    path('categories/', admin_categories_view, name='admin-categories'),
    path('subcategories/', admin_subcategories_view, name='admin-subcategories'),
    path('add-apps/', admin_add_apps_view, name='admin-add-apps'),
    path('tasks/', admin_task_list_view, name='admin-task-list'),
    path('users/', admin_user_list_view, name='admin-user-list'),
    path('app/<int:app_id>/', admin_app_detail_view, name='admin-app-detail'),
]