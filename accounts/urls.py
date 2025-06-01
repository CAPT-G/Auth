from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.index, name='home'),  # Optional landing page
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('verify/', views.verify_code_view, name='verify_code'),

    # Optional: Profile editing (if enabled)
    path('profile/', views.profile_view, name='profile'),

    # Optional: Resend confirmation code (if re-implemented for codes)
    path('resend/', views.resend_confirmation, name='resend_confirmation'),

    # Optional: Legacy token-based email confirmation (fallback)
    path('confirm/<uidb64>/<token>/', views.confirm_email_view, name='confirm_email'),
]

