from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import Apply_PassForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.template.loader import get_template
from xhtml2pdf import pisa
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
    context = {
        'objs' : obj
    }
    return render(request, 'core/apply_pass download_page.html', context)


def create_pdf(request):
    username = request.user
    obj = Apply_Pass.objects.get(passuser=username)

    template_path = 'core/download-page.html'
    context = {'objs' : obj}
    respons = HttpResponse(content_type='application/pdf')
    respons['Content-Disposition']='filename="report.pdf"'


    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=respons)
 
    if pisa_status.err:
        return HttpResponse('we had some errors <pre>'+html+'</pre>')
    return respons


def dashboard_view(request):
    total_registered_user = Registration.objects.all()
    new_applied_movement_pass_user = Apply_Pass.objects.order_by('-id')[:5]
    recent_registered = Registration.objects.order_by('-created_at')[:5]
    total_movement_pass = Apply_Pass.objects.all().count()
    total_movement_approved = Apply_Pass.objects.filter(is_approved=True).count()
    total_movement_pending = Apply_Pass.objects.filter(is_approved=False).count()
    total_movement_expire = Apply_Pass.objects.filter(is_expire=True).count()
    movement_reason = MovementReason.objects.all().count()
    total_district = District.objects.all().count()
    timelimit = TimeLimit.objects.all().count()

    context={
        'total_registered_user':total_registered_user,
        'recent_registered':recent_registered,
        'new_applied_movement_pass_user':new_applied_movement_pass_user,
        'total_movement_pass':total_movement_pass,
        'total_movement_approved':total_movement_approved,
        'total_movement_pending':total_movement_pending,
        'total_movement_expire':total_movement_expire,
        'movement_reason':movement_reason,
        'total_district':total_district,
        'timelimit':timelimit
    }

    return render(request, 'admina/dashboard.html', context)


class TimeLimitView(View):
    def get(self, request):
        timelimit = TimeLimit.objects.all()
        context = {
            'timelimit':timelimit
        }
        return render(request, 'admina/time.html', context)
    
    def post(self, request):
        time = request.POST['time']
        obj = TimeLimit.objects.create(time_limit=time)
        obj.save()
        return redirect('timelimit')

def delete_time(request, pk):
    obj = TimeLimit.objects.get(id=pk)
    obj.delete()
    return redirect('timelimit')


def all_movement_pass(request):
    all_pass = Apply_Pass.objects.all()
    context = {
        'all_pass': all_pass
    }
    return render(request, 'admina/all_movement_pass.html', context)


class SearchView(View):
    def get(self, request):
        search = request.GET.get('searched_item', None)
        obj = Apply_Pass.objects.all()
        if len(search)> 100 :
            obj_pass = obj.none()
        else:
            obj_pass = obj.filter(
                Q(passuser__registration__name__icontains = search) |
                Q(location_from__icontains = search) |
                Q(where_to__icontains = search) |
                Q(district__icontains = search) |
                Q(thana__icontains = search)
            )
        context ={
            'obj_pass':obj_pass,
            'search':search
        }
        
        return render(request, 'admina/search.html', context)