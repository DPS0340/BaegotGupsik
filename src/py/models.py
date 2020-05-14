from django.db import models

class menu(models.Model):
    id = models.IntegerField(primary_key=True)
    body = models.CharField(max_length=500)
