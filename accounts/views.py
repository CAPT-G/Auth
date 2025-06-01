from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import random
from datetime import timedelta

from .forms import SignUpForm, LoginForm, ProfileForm, ExtendedProfileForm, EmailVerificationForm
from .models import Profile, EmailVerification

User = get_user_model()


# 🔒 Helper to generate + send 6-digit code
def generate_verification_code():
    return str(random.randint(100000, 999999))


from .email_utils import send_verification_email_html

def send_verification_code(email):
    code = generate_verification_code()
    expires = timezone.now() + timedelta(minutes=10)
    EmailVerification.objects.update_or_create(
        email=email,
        defaults={
            'code': code,
            'expires_at': expires,
            'verified': False,
            'terms_accepted': False
        }
    )

    # Send HTML-styled branded email
    send_verification_email_html(email, code)

# 🟢 SIGNUP
@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']

            if User.objects.filter(email=email).exists():
                return render(request, 'accounts/modal_auth.html', {
                    'signup_form': form,
                    'login_form': LoginForm(),
                    'signup_error': 'Email already in use.',
                    'show_modal': 'signup'
                })

            try:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    is_active=False
                )
            except (ValidationError, IntegrityError) as e:
                return render(request, 'accounts/modal_auth.html', {
                    'signup_form': form,
                    'login_form': LoginForm(),
                    'signup_error': str(e),
                    'show_modal': 'signup'
                })

            send_verification_code(email)
            request.session['verify_email'] = email
            return redirect('accounts:verify_code')
    else:
        form = SignUpForm()

    return render(request, 'accounts/modal_auth.html', {
        'signup_form': form,
        'login_form': LoginForm(),
        'show_modal': 'signup'
    })


# 🟢 LOGIN
@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower()
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user and user.is_active:
                login(request, user)
                return redirect('accounts:dashboard')
            error = "Invalid credentials or account not verified."
            return render(request, 'accounts/modal_auth.html', {
                'login_form': form,
                'signup_form': SignUpForm(),
                'login_error': error,
                'show_modal': 'login'
            })
    else:
        form = LoginForm()

    return render(request, 'accounts/modal_auth.html', {
        'login_form': form,
        'signup_form': SignUpForm(),
        'show_modal': 'login'
    })


# 🟢 VERIFY CODE
@csrf_protect
def verify_code_view(request):
    email = request.session.get('verify_email')
    if not email:
        return redirect('accounts:signup')

    try:
        record = EmailVerification.objects.get(email=email)
    except EmailVerification.DoesNotExist:
        return redirect('accounts:signup')

    if request.method == 'POST':
        form = EmailVerificationForm(request.POST, email=email)
        if form.is_valid():
            record.verified = True
            record.terms_accepted = True
            record.save()

            user = User.objects.get(email=email)
            user.is_active = True
            user.save()

            login(request, user)
            del request.session['verify_email']
            return redirect('accounts:dashboard')
    else:
        form = EmailVerificationForm(email=email)

    return render(request, 'accounts/verify_code.html', {
        'form': form,
        'email': email
    })


# DASHBOARD / LOGOUT
@login_required
def dashboard_view(request):
    return render(request, 'accounts/dashboard.html')


@csrf_protect
def logout_view(request):
    logout(request)
    return redirect('accounts:login')
