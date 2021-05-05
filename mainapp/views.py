from django.shortcuts import render, redirect
from .models import Person
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.



def valid_pass(password):
    try:
        res = validate_password(password)
    except ValidationError as err:
        return str(err.messages)
    return None


def add_user(username, password):
    user: User = User.objects.create_user(username=username,
                                 email='',
                                 password=password)
    user.save()


def enterSecretCodeView(request):
    context = dict()
    codes = {
        '13032006': 'Sonya1.jpg',
        '08072005': 'Anya_i_Egor.jpg'
    }

    if request.method == 'POST' and 'code' in request.POST:
        code = str(request.POST['code'])
        if code in codes:
            context['image_name'] = codes[code]
    return render(request, 'mainapp/enter_secret_code.html', context=context)


def addFriendsView(request):
    if not request.user.is_authenticated:
        return redirect('/mainpage/register/', context={'message': 'Вы не вошли в систему!'})
    contxet = context={'users': Person.objects.all(),
                    'friends': request.user.person.friends.all()}
    context['main_user'] = request.user.person
    if request.method == 'POST':
        user_id = int(request.POST['name'])
        user = User.objects.get(id=user_id)
        if user and user != request.user:
            message = ''
            if user.person in request.user.person.friends_requests.all():
                request.user.person.friends.add(user.person)
                request.user.person.friends_requests.remove(user.person)
                message = f'Отлично, пользователь {user.person.name} теперь ваш друг!'
            else:
                user.person.friends_requests.add(request.user.person)
                message = f'Заявка в друзья пользователю {user.person.name} отправлена!'
            context['message'] = message

    return render(request, 'mainapp/add_friends.html', context=context)


def friendsRequestsView(request):
    if not request.user.is_authenticated:
        return redirect('/mainpage/register/', context={'message': 'Вы не вошли в систему!'})
    context = {'users': Person.objects.all(), 'fr_req': request.user.person.friends_requests.all()}
    if request.method == 'POST':
        user_id = int(request.POST['name'])

        user = User.objects.get(id=user_id)
        if user and user != request.user and user.person in request.user.person.friends_requests.all():
            request.user.person.friends.add(user.person)
            request.user.person.friends_requests.remove(user.person)
            message = f'Отлично, пользователь {user.person.name} теперь ваш друг!'
            context['message'] = message
    return render(request, 'mainapp/friends_requests.html', context=context)


def myFriendsView(request):
    if not request.user.is_authenticated:
        return redirect('/mainpage/register/', context={'message': 'Вы не вошли в систему!'})
    if request.method == 'POST' and 'name' in request.POST and 'action' in request.POST:
        user_id = int(request.POST['name'])
        user = User.objects.get(id=user_id)
        action = request.POST['action']
        if user and user != request.user and user.person in request.user.person.friends.all():
            print(user.person.depressions)
            print(request.user.person.depressions)
            if action == 'delete':
                request.user.person.friends.remove(user.person)
            elif action == 'add_depression':
                user.person.depressions = max(0, int(user.person.depressions) + 1)
            elif action == 'del_depression':
                user.person.depressions = max(0, int(user.person.depressions) - 1)
            user.person.save()
    return render(request, 'mainapp/my_friends.html', context={'users': Person.objects.all(),
                                    'friends': request.user.person.friends.all()})


def registrationView(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['psw']
        pass2 = request.POST['psw-repeat']
        err = None
        if pass1 != pass2:
            err = 'Password mismatch!'
        elif User.objects.filter(username=username).exists():
            err = 'Username already exists!'
        else:
            err = valid_pass(pass1)
        if err:
            return render(request, 'mainapp/registration.html', context={'error': err})
        else:
            add_user(username, pass1)
            return redirect('/accounts/login/')
    else:
        return render(request, 'mainapp/registration.html')


def mainView(request):
    return render(request, 'mainapp/index.html', context={'users': Person.objects.all()})