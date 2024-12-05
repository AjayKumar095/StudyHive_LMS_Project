from django.db import models

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
    course_duration = models.IntegerField(max_length=2)
    course_startdata = models.DateField()
    course_thumbnail = models.ImageField(upload_to='thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.course_title
    

    
