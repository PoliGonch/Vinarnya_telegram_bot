from django.db import models

# Create your models here.
class Wine(models.Model):
    liked = models.BooleanField()
    image = models.ImageField(upload_to=' vinarnya/images/')
    image_id = models.CharField(max_length=200, unique=True)
    color = models.ForeignKey('Color', on_delete=models.CASCADE, blank=True, null=True)
    type = models.ForeignKey('Type', on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey('Country', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, unique=True, blank=True, null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='wine')

class Color(models.Model):
    name_en = models.CharField(max_length=50, unique=True)
    name_uk = models.CharField(max_length=50, unique=True, blank=True, null=True)

class Type(models.Model):
    name_en = models.CharField(max_length=50, unique=True)
    name_uk = models.CharField(max_length=50, unique=True, blank=True, null=True)

class Country(models.Model):
    name_en = models.CharField(max_length=50, unique=True)
    name_uk = models.CharField(max_length=50, unique=True, blank=True, null=True)

class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

class User(models.Model):
    chat_id = models.IntegerField(unique=True)
    language = models.ForeignKey(Language, null=True, default=None, on_delete=models.SET_NULL)
    user_state = models.CharField(max_length=50, blank=True, null=True, default='Hello')



