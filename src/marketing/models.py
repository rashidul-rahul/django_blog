from django.db import models

# Create your models here.
class Signup(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __sr__(self):
        return self.email
    
