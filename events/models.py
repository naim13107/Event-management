from django.db import models 
from django.contrib.auth.models import User
# Create your models here. 
class Category(models.Model): 
    name = models.CharField(max_length=100) 
    description = models.TextField() 
    
    def __str__(self): 
        return self.name 
    
class Event(models.Model): 
    name = models.CharField(max_length=200) 
    description = models.TextField() 
    date = models.DateField() 
    time = models.TimeField() 
    location = models.CharField(max_length=150) 
    category = models.ForeignKey( 
        Category, 
        on_delete=models.CASCADE, 
        related_name='events') 
    participants = models.ManyToManyField(User, related_name='attended_events', blank=True)
    # image = models.ImageField(upload_to='event_image',)
    @property
    def image_file(self):
        mapping = {
            "Technology": "images/tech.webp",
            "Business": "images/business.webp",
            "Entertainment": "images/party.webp"
        }
        return mapping.get(self.category.name, "images/default.webp")


    
    def __str__(self): 
        return self.name 

# class Participant (models.Model):
#     name = models.CharField(max_length=200) 
#     email = models.EmailField() 
#     event = models.ManyToManyField( 
#         Event, 
#         related_name='participants' ) 
    
#     def __str__(self): 
#         return self.name
    
    