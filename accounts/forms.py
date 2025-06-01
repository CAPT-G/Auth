from django import forms
from .models import EmailVerification
from django.utils import timezone

class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={'placeholder': 'Enter 6-digit code'}),
        label='Verification Code'
    )
    terms_accepted = forms.BooleanField(
        required=True,
        label="I accept the Terms & Conditions"
    )

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
        terms_accepted = cleaned_data.get('terms_accepted')

        if not self.email:
            raise forms.ValidationError("Email context is missing.")

        try:
            record = EmailVerification.objects.get(email=self.email, code=code)
        except EmailVerification.DoesNotExist:
            raise forms.ValidationError("Invalid verification code.")

        if record.verified:
            raise forms.ValidationError("This email is already verified.")

        if record.is_expired():
            raise forms.ValidationError("This code has expired.")

        if not terms_accepted:
            raise forms.ValidationError("You must accept the Terms & Conditions to continue.")

        return cleaned_data
