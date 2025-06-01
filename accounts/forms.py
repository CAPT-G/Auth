from django import forms
from .models import EmailVerification


class SignUpForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class EmailVerificationForm(forms.Form):
    code = forms.CharField(max_length=6, min_length=6, label='Verification Code')
    terms_accepted = forms.BooleanField(required=True, label="I agree to the Terms and Conditions")

    def __init__(self, *args, **kwargs):
        self.email = kwargs.pop('email', None)
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data.get('code')
        if not code.isdigit():
            raise forms.ValidationError("Code must be 6 digits.")
        return code

    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('code')

        if not self.email:
            raise forms.ValidationError("Email not found in session.")

        try:
            record = EmailVerification.objects.get(email=self.email, code=code)
        except EmailVerification.DoesNotExist:
            raise forms.ValidationError("Invalid code.")

        if record.is_expired():
            raise forms.ValidationError("This code has expired.")

        if record.verified:
            raise forms.ValidationError("This email has already been verified.")
