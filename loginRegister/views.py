from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_list_or_404
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from properties.filters import PropertyFilter
from .models import Profile
from .forms import UserForm, LoginForm
from django.views import View
from properties.models import Property, PropertyImages, Enquiry


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
            return redirect('homepage')
        else:
            messages.add_message(self.request, messages.INFO, "Invalid username/password")
            return redirect('login')


def check_login(request):

    already_logged_in = request.session.get('logged_in', False)
    if not already_logged_in:
        return Login.as_view()(request)
    else:
        return redirect('/')


def logout_user(request):
    if not request.user.is_anonymous:
        logout(request)
        return redirect('/')
    else:
        messages.add_message(request, messages.INFO, "No User is logged in. Login first to logout!")
        return redirect('login')


class Dashboard(View):

    def get(self, request):
        return self.show_user()

    def show_user(self):
        username = self.request.session.get('current_user')
        is_seller = self.request.session.get('is_seller', False)
        try:
            current_user = Profile.objects.get(username=username)
            user = {'user': current_user}
            if is_seller:
                return self.show_seller(current_user, user)
            else:
                return self.show_buyer(current_user, user)
        except Profile.DoesNotExist:
            messages.add_message(self.request, messages.INFO, "Please Login first to view dashboard!")
            return redirect('login')

    def show_seller(self, current_user, context):
        queries_for_seller = []
        final_property = []
        try:
            posted_properties_images = []
            posted_properties = list(Property.objects.filter(property_owner_id=current_user.id))

            for property in posted_properties:
                posted_properties_images.append(PropertyImages.objects.filter(property_name__id=property.id)[0])
            final_property = zip(posted_properties, posted_properties_images)
            queries_for_seller = get_list_or_404(Enquiry, property__property_owner=current_user)
        except Property.DoesNotExist:
            posted_properties = False
            posted_properties_images = False
            final_property = False
        except Enquiry.DoesNotExist:
            queries_for_seller = False
        finally:
            context['queries_for_seller'] = queries_for_seller
            context['posted_properties'] = posted_properties
            context['posted_properties_image'] = posted_properties_images
            context['final_properties'] = final_property
            return render(self.request, 'dashboard_seller.html', context=context)

    def show_buyer(self, current_user, context):
        queries_made = []
        try:
            queries_made = get_list_or_404(Enquiry, requester=current_user)
        except Http404:
            queries_made = False
        finally:
            context['queries_made'] = queries_made
            return render(self.request, 'dashboard_buyer.html', context=context)

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


def queries(request,):
    context = {}
    username = request.session.get('current_user')
    queries_made = []
    try:
        queries_made = get_list_or_404(Enquiry, requester=username)
    except Http404:
        queries_made = False
    finally:
        context['queries_made'] = queries_made
        return render(request, 'queries.html', context=context)


def search(request):
    property_list = Property.objects.all()
    property_filter = PropertyFilter(request.GET, queryset=property_list)

    prop = property_filter.queryset
    prop_images = [PropertyImages.objects.filter(property_name=props) for props in prop]

    # import pdb; pdb.set_trace()
    return render(request, 'property_search.html', {'filter': property_filter, 'prop_images': prop_images})
