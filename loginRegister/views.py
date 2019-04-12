from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from .models import Profile
from .forms import UserForm, LoginForm
from django.views import View


# Create your views here.


@csrf_protect
def index(request):
    user = UserForm()

    context = {'form': user}

    return render(request, 'homepage.html')


class NewUser(FormView):

    form_class = UserForm
    template_name = 'registration_page.html'
    # success_url = '/success'

    def form_valid(self, form):
        import pdb; pdb.set_trace()
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
            # FIX this
            return redirect('dashboard')
        else:
            messages.add_message(self.request, messages.INFO, "Invalid username/password")
            return redirect('login')


def check_login(request):

    already_logged_in = request.session.get('logged_in', False)
    if not already_logged_in:
        return Login.as_view()(request)
    else:
        return redirect('dashboard')


def logout_user(request):
    if not request.user.is_anonymous:
        logout(request)
        return redirect('/login/')


class Dashboard(View):

    def get(self, request):
        return self.show_user()

    def show_user(self):
        username = self.request.session.get('current_user')
        try:
            current_user = Profile.objects.get(username=username)
            user = {'user': current_user}
            is_seller = self.request.session.get('is_seller', False)
            if is_seller:
                return render(self.request, 'dashboard.html', context=user)
            else:
                return render(self.request, 'dashboard.html', context=user)
        except Profile.DoesNotExist:
            messages.add_message(self.request, messages.INFO, "Please Login first to view dashboard!")
            return redirect('login')

    def post(self, request):
        username = self.request.session.get('current_user')
        current_user = Profile.objects.get(username=username)
        if request.POST.get('update_profile_button'):
            return render(request, 'update_user.html', {'user': current_user})
        elif request.POST.get('update_profile'):
            current_user.first_name = request.POST.get('first_name')
            current_user.last_name = request.POST.get('last_name')
            current_user.description = request.POST.get('description')
            if request.FILES.get('profile_pic'):
                current_user.profile_pic = request.FILES.get('profile_pic')
            current_user.save()
            return HttpResponse("Details updated!")
