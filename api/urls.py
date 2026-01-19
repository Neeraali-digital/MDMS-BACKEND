from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CollegeViewSet, EnquiryViewSet, AdminUserCreateView
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'colleges', CollegeViewSet)
router.register(r'enquiries', EnquiryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', obtain_auth_token, name='api_token_auth'),
    path('auth/create-admin/', AdminUserCreateView.as_view(), name='create_admin'),
]
