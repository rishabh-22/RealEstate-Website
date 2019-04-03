from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .forms import UserForm

# Create your views here.


@csrf_protect
def index(request):
    user = UserForm()

    context = {'UserForm': user}

    return render(request, 'registration_page.html', context)


def post(request):
    if request.method == 'POST':
        user = UserForm()
        if user.is_valid():
            user.save()
        else:
            return HttpResponse("invalid form!")
    return redirect('form')
