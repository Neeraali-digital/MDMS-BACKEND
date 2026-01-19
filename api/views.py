from rest_framework import viewsets, permissions
from .models import College, Enquiry
from rest_framework import generics
from .serializers import CollegeListSerializer, CollegeDetailSerializer, CollegeWriteSerializer, EnquirySerializer, AdminUserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.all()
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'type', 'featured']
    search_fields = ['name', 'location']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CollegeDetailSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return CollegeWriteSerializer
        return CollegeListSerializer

class EnquiryViewSet(viewsets.ModelViewSet):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer
    
    def get_permissions(self):
        if self.action == 'create':
             return [permissions.AllowAny()]
        # Only admin can view enquiries
        return [permissions.IsAdminUser()]

class AdminUserCreateView(generics.CreateAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.AllowAny] # Use with caution, for initial setup
