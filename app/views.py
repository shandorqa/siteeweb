"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from app.forms import ContactForm, FeedbackForm, RegistrationForm, CommentForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from app.models import Blog, Comment

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # получение данных
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            return render(
                request,
                'app/contact.html',
                {
                    'title':'Контакты',
                    'message':'Ваше сообщение успешно отправлено!',
                    'year':datetime.now().year,
                    'form': ContactForm(),
                    'submitted': True
                }
            )
    else:
        form = ContactForm()
    
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с вашими контактами.',
            'year':datetime.now().year,
            'form': form,
            'submitted': False
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о вас.',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the links page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ссылки',
            'year':datetime.now().year,
        }
    )

def pool(request):
    """Renders the feedback page."""
    assert isinstance(request, HttpRequest)
    
    submitted_data = None
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # получение
            submitted_data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'site_rating': form.cleaned_data['site_rating'],
                'usability_rating': form.cleaned_data['usability_rating'],
                'design_rating': form.cleaned_data['design_rating'],
                'liked_features': form.cleaned_data['liked_features'],
                'visit_frequency': form.cleaned_data['visit_frequency'],
                'feedback_text': form.cleaned_data['feedback_text'],
                'subscribe_news': form.cleaned_data['subscribe_news']
            }
            
            rating_text = {
                '1': 'Очень плохо',
                '2': 'Плохо',
                '3': 'Удовлетворительно',
                '4': 'Хорошо',
                '5': 'Отлично'
                
            }
            
            feature_text = {
                'design': 'Дизайн',
                'usability': 'Удобство использования',
                'information': 'Информативность',
                'tours': 'Выбор туров',
                'prices': 'Цены'
            }
            
            frequency_text = {
                'first_time': 'Первый раз',
                'rarely': 'Редко',
                'sometimes': 'Иногда',
                'often': 'Часто',
                'regular': 'Регулярно'
            }
            
            submitted_data['site_rating_text'] = rating_text.get(submitted_data['site_rating'], '')
            submitted_data['usability_rating_text'] = rating_text.get(submitted_data['usability_rating'], '')
            submitted_data['design_rating_text'] = rating_text.get(submitted_data['design_rating'], '')
            submitted_data['liked_features_text'] = [feature_text.get(feature, '') for feature in submitted_data['liked_features']]
            submitted_data['visit_frequency_text'] = frequency_text.get(submitted_data['visit_frequency'], '')
            
            return render(
                request,
                'app/pool.html',
                {
                    'title': 'Отзывы',
                    'message': 'Спасибо за ваш отзыв!',
                    'year': datetime.now().year,
                    'form': FeedbackForm(),
                    'submitted': True,
                    'submitted_data': submitted_data
                }
            )
    else:
        form = FeedbackForm()
    
    return render(
        request,
        'app/pool.html',
        {
            'title': 'Отзывы',
            'message': 'Оставьте свой отзыв о нашем сайте',
            'year': datetime.now().year,
            'form': form,
            'submitted': False
        }
    )

def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)
    if request.method == "POST": # после отправки формы
        regform = UserCreationForm(request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
            return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform, # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all()
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,
            'year': datetime.now().year,
        }
    )

def blogpost(request, parameter):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parameter)
    comments = Comment.objects.filter(post=post_1).order_by('-created')
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post_1
            comment.author = request.user
            comment.save()
            form = CommentForm()  # очистить форму после отправки
    else:
        form = CommentForm()
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )
