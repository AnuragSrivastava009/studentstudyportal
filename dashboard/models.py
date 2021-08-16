from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Notes(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField( max_length=50)
    description=models.TextField()
    
    def __str__(self):
        return self.title
        
    class Meta:

        verbose_name="notes"
        verbose_name_plural="notes"
#models for homework
class Homework(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField( max_length=100)
    subject=models.CharField(max_length=50)
    description=models.TextField()
    due=models.DateTimeField()
    is_finished=models.BooleanField(default=False)

    def __str__(self):
        return self.title


#model for todo

class TOdo(models.Model):
    User=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField( max_length=100)
    is_finished=models.BooleanField(default=False)
    
    def __str__(self):
        return self.title



