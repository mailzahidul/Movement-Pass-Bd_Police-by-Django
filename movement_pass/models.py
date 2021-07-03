from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class District(models.Model):
    district = models.CharField(max_length=20)

    def __str__(self):
        return self.district

class Gender(models.Model):
    gender = models.CharField(max_length=6)

    def __str__(self):
        return self.gender

class IdType(models.Model):
    id_type = models.CharField(max_length=20)

    def __str__(self):
        return self.id_type


class Registration(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=50)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    thana = models.CharField(max_length=50)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    date_of_birth = models.DateField()
    id_type = models.ForeignKey(IdType, on_delete=models.SET_NULL, null=True)
    id_number = models.PositiveIntegerField()
    created_at = models.DateField(auto_now_add=True)
    photo = models.ImageField(upload_to = 'user-registraion/')
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.name