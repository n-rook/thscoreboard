from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    email = forms.EmailField(label='email', max_length=200)
    password = forms.CharField(label='password', max_length=200, widget=forms.PasswordInput)

class RegisterFormWithPasscode(RegisterForm):
    passcode = forms.CharField(label='passcode', max_length=200)
    