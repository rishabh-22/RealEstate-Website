from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from .models import Profile
from .forms import UserForm, LoginForm

# Create your views here.


@csrf_protect
def index(request):
    user = UserForm()

    context = {'form': user}

    return render(request, 'login_page.html', context)


class NewUser(FormView):

    form_class = UserForm
    template_name = 'registration_page.html'
    # success_url = '/success'

    def form_valid(self, form):
        form.save()
        return HttpResponse('all set')

    def form_invalid(self, form):
        """if invalid return error and back to it"""
        return render(self.request, self.template_name, {'form': form, 'error': form.errors})


class Login(FormView):

    form_class = LoginForm
    template_name = 'login_page.html'

    def form_valid(self, form):

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        current_user = authenticate(request=self.request, username=username, password=password)
        if current_user is not None:
            login(self.request, current_user)
            self.request.session['logged_in'] = True
            self.request.session['current_user'] = username
            self.request.session['is_seller'] = Profile.objects.get(username=username).is_seller
            # import pdb;
            # pdb.set_trace()
            return HttpResponse('All set')
        else:
            return HttpResponse('invalid user')


def check_login(request):

    already_logged_in = request.session.get('logged_in', False)
    if not already_logged_in:
        return Login.as_view()(request)
    else:
        return HttpResponse('already logged in brother!')


def logout_user(request):
    if not request.user.is_anonymous:
        logout(request)
        return redirect('/login/')

