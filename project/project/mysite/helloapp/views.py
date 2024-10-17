from django.shortcuts import render
from django.http import HttpResponse
from .models import Books, AuthorMake

def hello(request,name):
    # cook = request.COOKIES
    # if 'count_visit' in request.session:
    #     request.session['count_visit'] += 1
    # else:
    #     request.session['count_visit'] = 1
    #
    # count_visit = request.session['count_visit']
    # resp = render(request, 'helloapp/index.html', context={'cook': cook, 'count_visit': count_visit})
    # resp.set_cookie("author", "Ivanusa")

    # ctxt = {'name': name}
    # return render(request, "helloapp/hello.html",ctxt)

    authors = AuthorMake.objects.all()
    books = Books.objects.all()
    print(authors, books)
    context = {
        'authors': authors,
        'books': books
    }
    return render(request, "helloapp/hello.html", context=context)


def id(request, number):
    return HttpResponse(f'Number {number}')

def req(request):
    name = request.GET['name']
    return HttpResponse(f'Name {name}')

def calc(request, a, b):
    return HttpResponse(f"A*B = {a*b}")
