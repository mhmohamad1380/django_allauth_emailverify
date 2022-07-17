from django.shortcuts import render
import datetime

from User.models import User
from django.utils import timezone
# Create your views here.
def home_page(request):
    
    context = {

    }
    if request.user.is_authenticated and request.user.is_verified == False:
        context['raise_activation_error'] = "Please Activate Your Email"
    return render(request,'home_page.html',context)