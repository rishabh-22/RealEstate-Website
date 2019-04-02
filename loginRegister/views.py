from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .forms import UserForm, ProfileForm

# Create your views here.


@csrf_protect
def index(request):
    user = UserForm()
    profile = ProfileForm()

    context = {'UserForm': user, 'ProfileForm': profile}

    return render(request, 'index_page.html', context)


def post(request):
    if request.method == 'POST':
        user = UserForm()
        profile = ProfileForm()
        if user.is_valid():
            user.save()
        if profile.is_valid():
            profile.save()
    return redirect('form')
