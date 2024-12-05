from django.db import models

# # model to add courese detail to index page

class indexdetails(models.Model):
    
    course_title = models.CharField(max_length=50)
    course_description = models.TextField(max_length=150)
    course_thumbnail = models.ImageField(upload_to='thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.course_title
    

    
