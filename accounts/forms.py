from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserCreationForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Имя', strip=False, required=True
    )
    email = forms.EmailField(
        label='email', required=True
    )
    password = forms.CharField(
        label='Пароль', strip=False, required=True, widget=forms.PasswordInput
    )
    password_confirm = forms.CharField(
        label='Подтвердить пароль', strip=False, required=True, widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError('Пароли не совпадают!')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = [
            'username', 'first_name', 'password', 'password_confirm', 'email'
        ]
