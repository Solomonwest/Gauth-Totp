from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import auth
from io import BytesIO
import qrcode
import qrcode.image.svg

from django.contrib import messages

from django_otp import login as otp_login
from django_otp.forms import OTPTokenForm
from django_otp.plugins.otp_totp.models import TOTPDevice


# Create your views here.
@login_required
def index(request):
    return render (request, 'index.html')


def totp_setup(request):

    confirmed_device = TOTPDevice.objects.filter(user=request.user, confirmed=True).first()
    if confirmed_device:
        return render


    device, created = TOTPDevice.objects.get_or_create(user=request.user, confirmed=False)

    otp_url = device.config_url
    # otp_key = device.key

    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(otp_url, image_factory=factory, box_size=20)

    stream = BytesIO()
    img.save(stream)
    svg_data = stream.getvalue().decode()


    token = request.POST.get('token','').strip()

    devices = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()

    if devices and devices.verify_token(token):
        devices.confirmed = True
        devices.save()
        return redirect('index')
    # else:
    #     return render(request, 'otp.html', {'error': "INVALID CODE"})

    return render(request, 'otp.html', {'qr_code':svg_data})


def verify_and_enable(request):
    token = request.POST.get('token','').strip()

    device = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()

    if device and device.verify_token(token):
        device.confirmed = True
        device.save()
        return redirect('index')
    else:
        return render(request, 'otp.html', {'error': "INVALID CODE"})


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
