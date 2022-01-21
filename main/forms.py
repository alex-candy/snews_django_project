from .models import *

from django import forms
import re

from django.forms import ModelForm, TextInput, DateTimeInput, Textarea
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
#
# class Kategori(forms.Form):
#     title = forms.CharField(max_length=255)
#     url_name = forms.CharField(max_length=255)
#     zamena = forms.CharField(max_length=255)
#
class Poisk(forms.Form):
    poisk = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'poisk'}))
#
class Koment(forms.Form):
    koment = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 5}))
#
# class AddNewsForm(forms.Form):
#     categor = forms.CharField(label="Категория новоcти")
#     title = forms.CharField(max_length=255, label="Заголовок", widget=forms.TextInput(attrs={'class': 'form-input'}))
#     slug = forms.SlugField(max_length=255, label="URL",widget=forms.TextInput(attrs={'class': 'form-input'}))
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label="Контент")
#     foto = forms.CharField( label="Путь к фото",widget=forms.TextInput(attrs={'class': 'form-foto-input'}),required=False)
#
# class UpdateNewsForm(forms.Form):
#     pole = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}))
#     redact = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
#
"""ФОРМА ДЛЯ СОЗДАНИЯ НОВОСТИ В ARTICLES"""
class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ['title','url','video_file','preview', 'full_text', 'condition', 'placing', 'type_video']

        widgets = {
            "title": TextInput(attrs={
                'class':'form-control',
            }),
            "url": TextInput(attrs={
                'class': 'form-control',
            }),
            'full_text': Textarea(attrs={
                'class': 'form-control',
            })

        }

"""ФОРМА ДЛЯ СОЗДАНИЯ НОВОСТИ В ARTICLES"""
class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']

        widgets = {
            "category_name": TextInput(attrs={
                'class':'form-control',
            })}


"""ФОРМА ДЛЯ СОЗДАНИЯ НОВОСТИ В VIDEO"""
class ArticlesForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['title','from_place','photo','full_text', 'category', 'condition', 'source']

        widgets = {
            "title": TextInput(attrs={
                'class':'form-control',
            }),
            "from_place": TextInput(attrs={
                'class': 'form-control',
            }),
            'full_text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст статьи'
            })

        }




#
# """ФОРМА ДЛЯ СОЗДАНИЯ СОТРУДНИКА"""
# class SotrudForm(ModelForm):
#     class Meta:
#         model = Sotrud
#         fields = ['foto','firstname','secondname','kontakts','role']
#
#         widgets = {
#             "firstname": TextInput(attrs={
#                 'class':'form-control',
#                 'placeholder': 'Имя'
#
#             }),
#             "secondname": TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Фамилия'
#
#             }),
#             "role": TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Должность'
#
#             }),
#             'kontakts': Textarea(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Можете указать любую контактную информацию'
#             })
#
#         }
#
#
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', help_text='Минимум 8 символов',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    # captcha = CaptchaField()


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail',
                             widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', help_text='Минимум 8 символов',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# # class NewsForm(forms.ModelForm):
# #     class Meta:
# #         model = News
# #         # fields = '__all__'
# #         fields = ['title', 'content', 'is_published', 'category']
# #         widgets = {
# #             'title': forms.TextInput(attrs={'class': 'form-control'}),
# #             'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
# #             'category': forms.Select(attrs={'class': 'form-control'}),
# #         }
# #
# #     def clean_title(self):
# #         title = self.cleaned_data['title']
# #         if re.match(r'\d', title):
# #             raise ValidationError('Название не должно начинаться с цифры')
# #         return title
#
#
