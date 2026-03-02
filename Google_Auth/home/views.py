from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import auth
from django.contrib import messages
from django.db import IntegrityError

from django_otp.plugins.otp_totp.models import TOTPDevice
from io import BytesIO
import qrcode
import qrcode.image.svg
import base64

from .forms import SignupForm, LoginForm  




# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except IntegrityError:
                # Handle rare race conditions or DB-level uniqueness failures
                form.add_error('username', 'A user with that username already exists.')
            else:
                print('FORM HAS BEEN SUCCESSFULLY CREATED')
                # login(request, user)
                return redirect('login')
        
    else:
        # GET: present an empty signup form
        form = SignupForm()

    return render(request, 'sign-up.html', {
        'form': form,
    })

@login_required
def index(request):
    return render (request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(request.user)
            return redirect('totp_setup')
        else:
            print('It worksssss!!!!')
            return messages.error(request, "User doesn't exist")

    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('login')


def totp_setup(request):
    confirmed_device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()
    if confirmed_device:
        return redirect( 'totp_verify')
    
    device, created = TOTPDevice.objects.get_or_create(user=request.user, confirmed=False)
    otp_url = device.config_url

    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(otp_url, image_factory=factory, box_size=20)
    stream = BytesIO()
    img.save(stream)

    # QR CODE for TOTP DEVICE 
    svg_data = stream.getvalue().decode()

    raw_key = device.bin_key
    # SECRET KEY FOR TOTP DEVICE
    base32_key = base64.b32encode(raw_key).decode('utf-8').strip('=')
    
    if request.method == 'POST':
        token = request.POST.get('token','').strip()

        devices = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()
        if devices and devices.verify_token(token):
            print(f"{request.user} is now verified. ")
            devices.confirmed = True
            devices.save()
            return redirect('index')
        
        else:

            return render(request, 'totp_setup.html', {'error': "INVALID CODE", 'qr_code':svg_data, 'setup_key': base32_key })

    # Delete all un-confirmed TOTP Devices for the user 
    TOTPDevice.objects.filter(user=request.user, confirmed=False).delete()
    device, created = TOTPDevice.objects.get_or_create(user=request.user, confirmed=False)

    return render(request, 'totp_setup.html', {'qr_code':svg_data, 'setup_key': base32_key})


def verify_and_enable(request):
    token = request.POST.get('token','').strip()

    device = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()

    if device and device.verify_token(token):
        device.confirmed = True
        device.save()
        return redirect('index')
    
    return render(request, 'totp_verify.html', {'error': "INVALID CODE"})



