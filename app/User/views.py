import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from .models import User
from User.forms import RegisterForm
import secrets
import string
from .tasks import sending_verification_email
import pytz
# Create your views here.


def login_page(request):
    
    context = {

    }
    return render(request, "users_login.html", context)


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("/")
    return HttpResponse("You are not Logged in !")


def register_page(request):
    if request.user.is_authenticated:
        return redirect("/")
    register_form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            token = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(128)) 
            User.objects.create_user(username=username, password=password,email=email,verify_token=token)
            filtered_user = User.objects.get(verify_token__iexact=token)
            filtered_user.verify_token_time += datetime.timedelta(days=1)
            filtered_user.save()
            sending_verification_email.delay(email,token)
            return redirect("/")
    return render(request, 'users_register.html', {
        "register_form": register_form
    })

def email_verify(request,*args,**kwargs):
    token = request.GET["email_verify"]
    filtered_user : User = User.objects.filter(verify_token__iexact=token)
    if filtered_user.exists():
        if filtered_user.first().is_verified == True:
            return HttpResponse("Your Account has been Activated Before!!!")
        else:
            a = filtered_user.first().verify_token_time.replace(tzinfo=pytz.UTC)
            b = datetime.datetime.now().replace(tzinfo=pytz.UTC)
            if a < b:
                return HttpResponse("Activation Link is not Valid anymore!!!")
            filtered_user.update(is_verified=True)
        return HttpResponse("Email has been Verified Seccussfully")
    return HttpResponse("something went error !")
