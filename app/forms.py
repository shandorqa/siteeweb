"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from .models import Comment

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class ContactForm(forms.Form):
    """Форма обратной связи."""
    name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        required=True,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput({
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )
    message = forms.CharField(
        label='Сообщение',
        required=True,
        min_length=10,
        max_length=500,
        widget=forms.Textarea({
            'class': 'form-control',
            'placeholder': 'Введите ваше сообщение',
            'rows': 5
        })
    )

class FeedbackForm(forms.Form):
    """Форма отзыва пользователя о сайте."""
    name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        required=True,
        widget=forms.TextInput({
            'class': 'form-control',
            'placeholder': 'Введите ваше имя'
        })
    )
    
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput({
            'class': 'form-control',
            'placeholder': 'Введите ваш email'
        })
    )
    
    RATING_CHOICES = [
        (1, '1 - Очень плохо'),
        (2, '2 - Плохо'),
        (3, '3 - Удовлетворительно'),
        (4, '4 - Хорошо'),
        (5, '5 - Отлично')
    ]
    
    site_rating = forms.ChoiceField(
        label='Общая оценка сайта',
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    
    usability_rating = forms.ChoiceField(
        label='Удобство использования',
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    design_rating = forms.ChoiceField(
        label='Дизайн сайта',
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    liked_features = forms.MultipleChoiceField(
        label='Что вам понравилось на сайте?',
        choices=[
            ('design', 'Дизайн'),
            ('usability', 'Удобство использования'),
            ('information', 'Информативность'),
            ('tours', 'Выбор туров'),
            ('prices', 'Цены')
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    visit_frequency = forms.ChoiceField(
        label='Как часто вы посещаете наш сайт?',
        choices=[
            ('first_time', 'Первый раз'),
            ('rarely', 'Редко'),
            ('sometimes', 'Иногда'),
            ('often', 'Часто'),
            ('regular', 'Регулярно')
        ],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    feedback_text = forms.CharField(
        label='Ваши пожелания и комментарии',
        required=False,
        min_length=1,
        max_length=1000,
        widget=forms.Textarea({
            'class': 'form-control',
            'placeholder': 'Поделитесь своими впечатлениями и предложениями',
            'rows': 5
        })
    )
    
    subscribe_news = forms.BooleanField(
        label='Подписаться на новости и специальные предложения',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        labels = {'text': 'Комментарий'}
