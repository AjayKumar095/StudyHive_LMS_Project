from django.contrib import admin
from django.contrib.admin.sites import site
from AdminWorkFlow.models import indexdetails

## Admin work

class indexdetailsAdmin(admin.ModelAdmin):
    list_display = ('course_title', 'course_description', 'course_thumbnail')
    

admin.site.register(indexdetails, indexdetailsAdmin)    
