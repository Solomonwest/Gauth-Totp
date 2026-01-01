from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from django_otp.decorators import otp_required
from django_otp import login as otp_login
from django_otp.forms import OTPTokenForm


# Create your views here.
@login_required
@otp_required
def index(request):
    return render (request, 'index.html')


def otp_verify(request):

    user = request.user
    if request.method == 'POST':
        form = OTPTokenForm(user, request.POST)
        if form.is_valid():
            otp_login(request, form.otp_device)
            return redirect ('home')
        
    else:
        form = OTPTokenForm(user)

    return render(request, 'otp.html', {'form':form})

