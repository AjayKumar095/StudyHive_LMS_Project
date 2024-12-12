import os
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_video_file(value):
    # Define the allowed video file extensions
    valid_extensions = ['mp4', 'avi', 'mov', 'mkv', 'flv', 'webm']
    extension = value.name.split('.')[-1].lower()
    if extension not in valid_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed extensions: {', '.join(valid_extensions)}")
    
def validate_pdf(value):
    # Check if the file is a PDF based on the file extension
    if not value.name.endswith('.pdf'):
        raise ValidationError('File must be a PDF.')
    
# # model to add courese detail to index page     
class CourseDetails(models.Model):
    
    course_language_choice = [
        ('English', 'English'),
        ('Hindi', 'Hindi'),
        ('Hinglish', 'Hinglish'),
    ]
    
    course_title = models.CharField(max_length=50)
    course_description = models.TextField(max_length=150)
    course_long_description = models.TextField(max_length=300)
    course_price = models.FloatField(max_length=6)
    course_language = models.CharField(max_length=20, choices=course_language_choice, default='English')
    course_duration = models.IntegerField()
    course_startdata = models.DateField()
    course_thumbnail = models.ImageField(upload_to='thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.course_title
    

## model for course purchase    
class course_purchase_by_user(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetails, on_delete=models.CASCADE, related_name='Purchased_course_id')
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Course price
    purchase_date = models.DateTimeField(auto_now_add=True)  # Auto-add timestamp

    def __str__(self):
        return f"{self.user.username} purchased {self.course.course_title}"
    
# Video model for storing video files
class Add_Video(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='videos/', validators=[validate_video_file])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(CourseDetails, related_name='videos', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.course.course_title}"


# Assignment model for storing assignments (e.g., PDFs, Word files)
class Add_Assignment(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='assignments/', validators=[validate_pdf])
    uploaded_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(CourseDetails, related_name='assignments', on_delete=models.CASCADE)
    marks = models.IntegerField(null=True, blank=True)  # Marks assigned for the assignment
    
    def __str__(self):
        return f"{self.title} - {self.course.course_title}"



## Assignment submit by user model
class Assignment_submit(models.Model):
    
    title = models.CharField(max_length=50)
    pdf_file = models.FileField(upload_to='User_submition/', validators=[validate_pdf])
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetails, on_delete=models.CASCADE)
    uploaded_at = models.DateField(auto_now_add=True)
    obtained_marks = models.IntegerField(null=True, blank=True)  # Marks obtained by the student, editable in admin
    
    class Meta:
        unique_together = ('user', 'title')  # Ensure unique constraint

    def delete_old_file(self):
        # Delete the old file from the storage
        if self.pdf_file and os.path.isfile(self.pdf_file.path):
            os.remove(self.pdf_file.path)

    def __str__(self):
        return f"{self.user.username} - {self.title}"

## model for user help or query
class Userquery(models.Model):
    
    username = models.CharField(max_length=25)
    email = models.EmailField()
    query_type = models.CharField(max_length=50)
    query = models.TextField()
    Date = models.DateField(auto_now_add=True)


    