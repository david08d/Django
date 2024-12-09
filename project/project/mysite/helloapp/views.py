# from django.contrib.auth import login
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
# from django.shortcuts import render, redirect
# from django.http import HttpResponse
#
# from .forms import EditUserForm, EditProfileForm
#
# from .models import Books, AuthorMake, Profile
#
#
# def hello(request,name):
#     # cook = request.COOKIES
#     # if 'count_visit' in request.session:
#     #     request.session['count_visit'] += 1
#     # else:
#     #     request.session['count_visit'] = 1
#     #
#     # count_visit = request.session['count_visit']
#     # resp = render(request, 'helloapp/index.html', context={'cook': cook, 'count_visit': count_visit})
#     # resp.set_cookie("author", "Ivanusa")
#
#     # ctxt = {'name': name}
#     # return render(request, "helloapp/hello.html",ctxt)
#
#     authors = AuthorMake.objects.all()
#     books = Books.objects.all()
#     print(authors, books)
#     context = {
#         'authors': authors,
#         'books': books
#     }
#     return render(request, "helloapp/hello.html", context=context)
#
#
# def id(request, number):
#     return HttpResponse(f'Number {number}')
#
# def req(request):
#     name = request.GET['name']
#     return HttpResponse(f'Name {name}')
#
# def calc(request, a, b):
#     return HttpResponse(f"A*B = {a*b}")
#
#
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             Profile.objects.create(user=user)
#             login(request, user)  # Log in the user immediately after registration
#             return redirect('helloapp/index.html')  # Redirect to a 'home' page after registration
#     else:
#         form = UserCreationForm()
#     return render(request, 'helloapp/register.html', {'form': form})
# def open_page(request):
#     return HttpResponse("<h1>Open page</h1><p> This page is available to everyone without any restrictions. Enjoy!</p>")
# @login_required
# def closed_page(request):
#     return HttpResponse("<h1>Closed page</h1><p>This page is available only to authorized users. <br> You are definitely authorized if you see this page.</p>")
# @login_required
# def edit_account(request):
#     # user = User.objects.get(pk=request.user.id)
#     if request.method == "POST":
#         user_edit_form = EditUserForm(instance=request.user,
#                                       data = request.POST)
#         profile_edit_form = EditProfileForm(instance=request.user.profile,
#                                             data = request.POST,
#                                             files = request.FILES)
#
#         if user_edit_form.is_valid() and profile_edit_form.is_valid():
#             user_edit_form.save()
#             profile_edit_form.save()
#     else:
#         user_edit_form = EditUserForm(instance=request.user)
#         profile_edit_form = EditProfileForm(instance=request.user.profile)
#
#     return render(request,
#                   'registration/account_edit_form.html',
#                   {
#
#                       "user_edit_form" : user_edit_form,
#                       "profile_edit_form" : profile_edit_form
#                   })
#


from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import EditUserForm, EditProfileForm
from .models import Books, AuthorMake, Profile


def hello(request, name):
    """Виведення списку авторів і книг."""
    authors = AuthorMake.objects.all()
    books = Books.objects.all()
    context = {
        'authors': authors,
        'books': books
    }
    return render(request, "helloapp/hello.html", context=context)


def id(request, number):
    """Виведення числа з URL."""
    return HttpResponse(f'Number {number}')


def req(request):
    """Отримання значення параметра 'name' з URL."""
    name = request.GET.get('name', 'Anonymous')
    return HttpResponse(f'Name {name}')


def calc(request, a, b):
    """Множення двох чисел."""
    return HttpResponse(f"A*B = {a * b}")


def register(request):
    """Реєстрація нового користувача."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            if profile:
                login(request, user)
                return redirect('helloapp:hello', name=user.username)
    else:
        form = UserCreationForm()
    return render(request, 'helloapp/register.html', {'form': form})


def open_page(request):
    """Сторінка, доступна для всіх."""
    return HttpResponse("<h1>Open page</h1><p>This page is available to everyone without any restrictions. Enjoy!</p>")


@login_required
def closed_page(request):
    """Сторінка, доступна лише авторизованим користувачам."""
    return HttpResponse("<h1>Closed page</h1><p>This page is available only to authorized users.</p>")

@login_required
def edit_account(request):
    # Перевірка наявності профілю
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_edit_form = EditUserForm(instance=request.user, data=request.POST)
        profile_edit_form = EditProfileForm(instance=profile, data=request.POST, files=request.FILES)

        if user_edit_form.is_valid() and profile_edit_form.is_valid():
            user_edit_form.save()
            profile_edit_form.save()
    else:
        user_edit_form = EditUserForm(instance=request.user)
        profile_edit_form = EditProfileForm(instance=profile)

    return render(
        request,
        'helloapp/account_edit_form.html',
        {
            "user_edit_form": user_edit_form,
            "profile_edit_form": profile_edit_form
        }
    )
