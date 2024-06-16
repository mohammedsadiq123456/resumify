from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    years_of_experience = models.FloatField()
    skills = models.TextField()

    def __str__(self):
        return self.name
