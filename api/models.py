from django.db import models

class College(models.Model):
    CATEGORY_CHOICES = [
        ('medical', 'Medical'),
        ('dental', 'Dental'),
        ('ayurveda', 'Ayurveda'),
        ('homeo', 'Homeo'),
        ('naturopathy', 'Naturopathy'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='medical')
    image = models.ImageField(upload_to='colleges/', null=True, blank=True)
    # For compatibility with frontend expecting a URL directly
    image_url = models.URLField(max_length=500, blank=True, null=True, help_text="External URL if not uploading image")
    description = models.TextField()
    featured = models.BooleanField(default=False)
    
    # Extra fields for details page
    hero_image = models.ImageField(upload_to='colleges/hero/', null=True, blank=True)
    about = models.TextField(blank=True)
    highlights = models.JSONField(default=list, blank=True) # List of strings
    gallery = models.JSONField(default=list, blank=True) # List of image URLs


    def __str__(self):
        return self.name

    @property
    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url

class Course(models.Model):
    college = models.ForeignKey(College, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    duration = models.CharField(max_length=50, blank=True)
    seats = models.CharField(max_length=50, blank=True)
    fees = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} - {self.college.name}"

class Enquiry(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    message = models.TextField(blank=True)
    college = models.ForeignKey(College, related_name='enquiries', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.name} ({self.created_at})"
