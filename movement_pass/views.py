from django.shortcuts import render, redirect
from django.views import View
from .models import District, Gender, IdType, Registration, Apply_Pass
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import Apply_PassForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.

def home(request):  
    return render(request, 'pages/home.html')


def userlogin(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        date_of_birth = request.POST['date_of_birth']
        user = authenticate(username=phone, password=date_of_birth)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
                messages.success(request, "Login Success")
            return redirect('home')
        else:
            messages.error(request, "Phone or Date of Birth invalid")
    return render(request, 'core/login.html')

def userlogout(request):
    logout(request)
    return redirect('home')

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
        photo = request.FILES.get('photo')
        if password1 != password2:
            messages.error(request, "Password not match...")

        has_account = Registration.objects.filter(user=phone)
        if has_account:
            messages.error(request, phone+" Already Exist.")
        try:
            new_user = User.objects.create_user(username=phone, password=date_of_birth)
            regi = Registration(user=new_user, name=name, district=district_get, thana=thana, gender=gender_get, date_of_birth=date_of_birth, id_type=id_type_get, id_number=id_number, photo=photo)
            regi.save()
            messages.success(request, "Ragistration success")  
        except Exception as errors:
            messages.error(request, phone+" Already Exist.")
            return redirect('registration')             
        return redirect('home')

@method_decorator(login_required, name='dispatch')
class ApplyPassView(View):
    def get(self, request):
        forms = Apply_PassForm()
        context = {
            'forms':forms
        }
        return render(request, 'core/apply_pass.html', context)
    
    def post(self, request):
        forms = Apply_PassForm(request.POST)
        username = request.user
        if forms.is_valid():
            obj = forms.save(commit=False)
            obj.passuser=username
            obj.save()
            messages.success(request, "Apply for pass success")
            return redirect('home')
        else:
            messages.error(request, "Invalid Value")
        return render(request, 'core/apply_pass.html')


class ApplyPassList(View):
    def get(self, request):
        username = request.user
        obj = Apply_Pass.objects.filter(passuser=username)
        context = {
            'objs' : obj
        }
        return render(request, 'core/apply_pass_list.html', context)

def apply_pass_download_page(request):
    username = request.user
    obj = Apply_Pass.objects.get(passuser=username)
    print(obj.passuser.registration)
    # print(obj.passuser.__registration,"Check")
    # obj = Registration.objects.get(user=username)
    print(obj, "MINA")
    context = {
        'objs' : obj
    }
    return render(request, 'core/apply_pass download_page.html', context)