from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import auth
from django.contrib import messages

from django_otp.plugins.otp_totp.models import TOTPDevice
from io import BytesIO
import qrcode
import qrcode.image.svg
import base64

from .forms import SignupForm, LoginForm  




# Create your views here.


def signup(request):
    if request.method == 'POST':
        if 'login_submit' in request.POST:
            form = SignupForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('/')

    return render(request, 'sign-up.html',{
        'form' : form,
    })

@login_required
def index(request):
    return render (request, 'index.html')


def totp_setup(request):

    confirmed_device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()
    if confirmed_device:
        return render(request, 'totp_verify.html',
                      {'has_confirmed_device': True})
    
    # Delete all un-confirmed TOTP Devices for the user 
    TOTPDevice.objects.filter(user=request.user, confirmed=False).delete()


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


    token = request.POST.get('token','').strip()

    devices = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()

    if devices and devices.verify_token(token):
        devices.confirmed = True
        devices.save()
        return redirect('index')
    # else:
    #     return render(request, 'otp.html', {'error': "INVALID CODE"})

    return render(request, 'otp.html', {'qr_code':svg_data, 'setup_key': base32_key})


def verify_and_enable(request):
    token = request.POST.get('token','').strip()

    device = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()

    if device and device.verify_token(token):
        device.confirmed = True
        device.save()
        return redirect('index')
    else:
        return render(request, 'totp_verify.html', {'error': "INVALID CODE"})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(request.user)
            return redirect('index')
        else:
            print('It worksssss!!!!')
            return messages.error(request, "User doesn't exist")

    return render(request, 'login.html')

def logout(request):
    user = request.user
    auth.logout(user)
    return redirect('login')
