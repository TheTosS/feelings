# feelingss/forms.py
from django import forms
from .models import Feeling
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Улучшаем внешний вид форм
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FeelingForm(forms.ModelForm):
    class Meta:
        model = Feeling
        fields = ['text', 'emotion']
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Что вы чувствуете сегодня? Поделитесь своими эмоциями...',
                'rows': 4,
                'class': 'form-control'
            }),
            'emotion': forms.Select(attrs={
                'class': 'form-control'
            })
        }
        labels = {
            'text': 'Ваши чувства',
            'emotion': 'Основная эмоция'
        }