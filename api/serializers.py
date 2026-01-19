from rest_framework import serializers
from .models import College, Course, Enquiry

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'duration', 'seats', 'fees']

class CollegeListSerializer(serializers.ModelSerializer):
    courses = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = College
        fields = ['id', 'name', 'slug', 'location', 'type', 'category', 'image', 'description', 'courses', 'featured']

    def get_courses(self, obj):
        return obj.courses.values_list('name', flat=True)

    def get_image(self, obj):
        return obj.get_image

class CollegeDetailSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    image = serializers.SerializerMethodField()
    heroImage = serializers.SerializerMethodField()

    class Meta:
        model = College
        fields = ['id', 'name', 'slug', 'location', 'type', 'category', 'image', 'heroImage', 'description', 'featured', 'about', 'highlights', 'gallery', 'courses']

    def get_image(self, obj):
        return obj.get_image
    
    def get_heroImage(self, obj):
        # Fallback to the main image since we merged the inputs
        if obj.hero_image:
            return obj.hero_image.url
        return obj.get_image

class CollegeWriteSerializer(serializers.ModelSerializer):
    courses = serializers.JSONField(write_only=True, required=False)  # Accept courses as JSON string/list
    gallery_files = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = College
        fields = ['name', 'slug', 'location', 'type', 'category', 'image', 'description', 'featured', 'about', 'highlights', 'gallery', 'gallery_files', 'courses', 'image_url']

    def create(self, validated_data):
        courses_data = validated_data.pop('courses', [])
        gallery_files = validated_data.pop('gallery_files', [])
        
        # Handle Gallery Files
        gallery_urls = validated_data.get('gallery', [])
        if gallery_files:
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile
            import os
            
            for file in gallery_files:
                file_path = f"colleges/gallery/{file.name}"
                saved_path = default_storage.save(file_path, ContentFile(file.read()))
                # Construct URL (assuming MEDIA_URL is /media/)
                url = f"/media/{saved_path}"
                gallery_urls.append(url)
            
            # Limit to 4 images if enforcing strict limit
            gallery_urls = gallery_urls[:4]
            validated_data['gallery'] = gallery_urls

        college = College.objects.create(**validated_data)
        
        if courses_data:
            import json
            if isinstance(courses_data, str):
                courses_data = json.loads(courses_data)
            for course_data in courses_data:
                Course.objects.create(college=college, **course_data)
        
        return college

    def update(self, instance, validated_data):
        courses_data = validated_data.pop('courses', None)
        gallery_files = validated_data.pop('gallery_files', None)
        
        # Handle Gallery Files Upload
        if gallery_files:
            from django.core.files.storage import default_storage
            from django.core.files.base import ContentFile
            
            current_gallery = instance.gallery or []
            for file in gallery_files:
                file_path = f"colleges/gallery/{file.name}"
                saved_path = default_storage.save(file_path, ContentFile(file.read()))
                url = f"/media/{saved_path}"
                current_gallery.append(url)
            
            # Update instance gallery
            instance.gallery = current_gallery[:4] # Enforce limit
        
        # Update standard fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update courses if provided (Complete replacement strategy for simplicity)
        if courses_data is not None:
            import json
            if isinstance(courses_data, str):
                courses_data = json.loads(courses_data)
            
            instance.courses.all().delete()
            for course_data in courses_data:
                Course.objects.create(college=instance, **course_data)
                
        return instance

class EnquirySerializer(serializers.ModelSerializer):
    college_name = serializers.CharField(source='college.name', read_only=True)
    class Meta:
        model = Enquiry
        fields = ['id', 'name', 'phone', 'email', 'message', 'enquiry_type', 'college', 'college_name', 'created_at']

from django.contrib.auth import get_user_model
User = get_user_model()

class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_superuser(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user
