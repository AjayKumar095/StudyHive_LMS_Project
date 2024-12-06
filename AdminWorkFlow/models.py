from django.db import models
from django.contrib.auth.models import User

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
    

    
class course_purchase_by_user(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseDetails, on_delete=models.CASCADE, related_name='Purchased_course_id')
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Course price
    purchase_date = models.DateTimeField(auto_now_add=True)  # Auto-add timestamp

    def __str__(self):
        return f"{self.user.username} purchased {self.course.name}"