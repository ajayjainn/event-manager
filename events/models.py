from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    organizer = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    desc = models.TextField()
    date = models.DateField(null=True)
    code = models.CharField(default=None,max_length=20)
    user = models.ManyToManyField(User,blank=True,related_name='invitees')

    def __str__(self):
        return self.name
