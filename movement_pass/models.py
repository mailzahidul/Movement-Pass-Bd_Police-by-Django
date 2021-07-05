from django.db import models
from django.contrib.auth.models import User
import uuid
# Qrcode Generator import 
import qrcode 
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


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


class TimeLimit(models.Model):
    time_limit = models.PositiveIntegerField()

    def __str__(self):
        return str(self.time_limit)


class MovementType(models.Model):
    movement_type = models.CharField(max_length=50)

    def __str__(self):
        return self.movement_type

class MovementReason(models.Model):
    movement_reason = models.CharField(max_length=50)

    def __str__(self):
        return self.movement_reason



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

class Apply_Pass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    passuser = models.OneToOneField(User, on_delete = models.SET_NULL, null=True)
    location_from = models.CharField(max_length=50)
    where_to = models.CharField(max_length=50)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True)
    thana = models.CharField(max_length=50)
    journey_date = models.DateTimeField()
    qr_image = models.ImageField(upload_to='qr/', null=True,blank=True)
    time_limit = models.ForeignKey(TimeLimit, on_delete=models.SET_NULL, null=True)
    movement_type = models.ForeignKey(MovementType, on_delete=models.SET_NULL, null=True)
    movement_reason = models.ForeignKey(MovementReason, on_delete=models.SET_NULL, null=True)
    applied_date = models.DateField(auto_now=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.passuser.registration.name


    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.id)
        canvas = Image.new('RGB', (410, 410), 'white')
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.id}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_image.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

    # def save(self,*args,**kwargs):
    #     qrcode_img = qrcode.make(self.id)
    #     canvas = Image.new('RGB',(290, 290),'white')
    #     draw = ImageDraw.Draw(canvas)
    #     canvas.paste(qrcode_img)
    #     frame = f'qr_code-{self.id}.png'
    #     buffer = BytesIO()
    #     canvas.save(buffer,'PNG')
    #     self.qr_image.save(frame, File(buffer), save=False)
    #     canvas.close()
    #     super().save(*args,**kwargs)
