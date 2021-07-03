from django.shortcuts import render, redirect
from django.views import View
from .models import District, Gender, IdType, Registration
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def home(request):
    return render(request, 'pages/home.html')


def userlogin(request):
    return render(request, 'core/login.html')


class RegistrationView(View):

    def get(self, request):
        district = District.objects.all()
        gender = Gender.objects.all()
        id_type = IdType.objects.all()
        context = {
            'district' : district,
            'gender' : gender,
            'id_type' : id_type
        }
        return render(request, 'core/registration.html', context)
    
    def post(self, request):
        name = request.POST['name']
        phone = request.POST['phone']
        district = request.POST['district']
        district_get = District.objects.get(district=district)
        thana = request.POST['thana']
        gender = request.POST['gender']
        gender_get = Gender.objects.get(gender=gender)
        date_of_birth = request.POST['date_of_birth']
        id_type = request.POST['id_type']
        id_type_get = IdType.objects.get(id_type=id_type)
        id_number = request.POST['id_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        photo = request.POST.get('photo')
        print("Before Password match")
        if password1 != password2:
            messages.danger(request, "Password not match...")
        print("Before auth_info")
        auth_info={
            'username':phone,
            'password':password1
            }
        new_user = User(**auth_info)
        new_user.save()
        print("Before data save")
        regi = Registration(name=name, user=new_user, district=district_get, thana=thana, gender=gender_get, date_of_birth=date_of_birth, id_type=id_type_get, id_number=id_number, photo=photo)
        regi.save()
        messages.success(request, "Ragistration success")        
        return redirect('home')
