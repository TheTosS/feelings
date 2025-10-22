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
                'placeholder': 'Опишите подробно, что вы чувствуете сегодня... 💫\nНапример: "Сегодня я чувствую себя прекрасно! Встретил старого друга и провел отличный день на природе."',
                'rows': 5,
                'class': 'form-control',
                'maxlength': '1000'
            }),
            'emotion': forms.Select(attrs={
                'class': 'form-control form-select'
            })
        }
        labels = {
            'text': 'Ваши чувства',
            'emotion': 'Основная эмоция'
        }

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text.strip()) < 5:
            raise forms.ValidationError('Пожалуйста, напишите хотя бы несколько слов о ваших чувствах.')
        return text


