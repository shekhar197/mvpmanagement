from django.http import HttpResponse
from django.shortcuts import render,redirect
from ..forms import UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your views here.

@login_required
def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user_detail = User.objects.all()
            return render(request, 'mvpManagement/home.html',{'user_detail':user_detail})
        elif request.user.usertype == '1':
            return render(request, 'mvpManagement/home.html')


