from django.contrib import admin
from .models import College, Course, Enquiry

class CourseInline(admin.TabularInline):
    model = Course
    extra = 1

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'type', 'featured')
    search_fields = ('name', 'location')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [CourseInline]

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'college', 'created_at')
    list_filter = ('created_at', 'college')
    search_fields = ('name', 'phone', 'email')
