from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView
from loginRegister.models import Profile
from .forms import PropertyForm, PropertyImagesForm
from .models import PropertyImages, Property, Enquiry
from django.contrib import messages
from .filters import PropertyFilter


def check_session(request, *args):

    flag = True
    for arg in args:
        flag = flag and request.session.get(arg, False)
    return flag


class CreateNewProperty(View):

    def get(self, request):
        if check_session(request, 'logged_in', 'is_seller'):
            context = {
                'property_form': PropertyForm(),
                'property_images': PropertyImagesForm()
            }
            return render(request, 'property_register.html', context=context)
        elif check_session(request, 'logged_in'):
            messages.add_message(request, messages.INFO, "Not Logged In, Please login as seller to post a property")
            return redirect('login')

    def post(self, request):

        images_uploaded = self.request.FILES.getlist('Property_Images')
        form_data = PropertyForm(self.request.POST)
        if form_data.is_valid():
            property_form = form_data.save(commit=False)
            property_form.property_owner_id = self.request.user.id
            property_form.save()
            for i in range(len(images_uploaded)):
                PropertyImages.objects.create(property_image=images_uploaded[i], property_name_id=property_form.id)
            return HttpResponse('all set')
        else:
            return HttpResponse(form_data.errors)


class ExistingProperty(View):

    def get(self, request, id):
        property = Property.objects.get(pk=id)
        property_images = PropertyImages.objects.filter(property_name_id=property.id)
        no_of_images = len(property_images)
        current_user = request.session.get('current_user')
        property_owner = property.property_owner
        context = {'property': property, 'property_images': property_images, 'no_of_images': range(no_of_images)}
        if check_session(request, 'logged_in'):
            is_seller = check_session(request, 'is_seller')
            context['logged_in'] = True
            if is_seller:
                # return render(request, 'property_display.html', context=context)
                return show_property_for_seller(request, context, current_user, property_owner)
            else:
                return show_property_for_buyer(request, context, current_user, property)
                # return render(request, 'property_update.html', context=context)
            # return render(request, 'property_display.html', context=context)
        return render(request, 'property_display.html', context=context)
        # messages.add_message(request, messages.INFO, "Not Logged In, Please login to view the property")
        # return redirect('login')

    def post(self, request, id):
        current_property = Property.objects.get(pk=id)
        current_user_value = User.objects.get(username=request.session.get('current_user'))
        current_user = Profile.objects.get(user=current_user_value)
        if self.request.POST.get('update_property'):
            images_uploaded = self.request.FILES.getlist('property_images')
            form_data = PropertyForm(self.request.POST)
            if form_data.is_valid():
                property_form = form_data.save(commit=False)
                property_form.property_owner_id = self.request.user.id
                string_fields = ['property_title',
                                 'property_address',
                                 'property_description']
                int_fields = ['property_pin',
                              'property_price',
                              'property_bedrooms',
                              'property_bathrooms',
                              'property_sqFeet',
                              'property_lotSize',
                              'property_garage',
                              ]
                for field in string_fields:
                    setattr(current_property, field, self.request.POST.get(field))
                for field in int_fields:
                    setattr(current_property, field, int(self.request.POST.get(field)))
                current_property.save()
                PropertyImages.objects.filter(property_name_id=current_property.id).delete()
                for i in range(len(images_uploaded)):
                    PropertyImages.objects.create(property_image=images_uploaded[i], property_name_id=current_property.id)
                return HttpResponse('Property updated Successfully!')
            else:
                return HttpResponse(form_data.errors)
        elif request.POST.get('submit_query'):
            return handle_query(request, current_property, current_user, id)


def show_property_for_seller(request, context, current_user, property_owner):
    if current_user == str(property_owner):
        return render(request, 'property_update.html', context=context)
    else:
        return render(request, 'property_display.html', context=context)


def show_property_for_buyer(request, context, current_user, current_property):
    context['is_buyer'] = True
    current_user = User.objects.get(username=current_user)
    try:
        Enquiry.objects.get(property=current_property, requester=current_user)
        return render(request, 'property_display.html', context=context)
    except Enquiry.DoesNotExist:
        context['no_query_made'] = True
        return render(request, 'property_display.html', context=context)


class UpdateProperty(UpdateView):

    model = Property
    form_class = PropertyForm
    template_name = 'property_form.html'

    def get(self, request, *args, **kwargs):
        """
        Method to handle and decide whether allowing the logged in user to update the property or not
        :return: Either the form containing values to update the properties or login page to login as seller
        """

        if self.request.session.get('logged_in', False):

            current_property = Property.objects.get(pk=self.get_object().id)
            current_user = User.objects.get(username=self.request.session.get('current_user'))
            if current_property.property_owner == current_user:
                return super().get(request, *args, **kwargs)
            else:
                logout(self.request)
                messages.add_message(self.request, messages.INFO, "Please login as seller to post a property")
                return redirect('login')
        else:
            messages.add_message(self.request, messages.INFO,
                                 "Not Logged In, Please login as seller to update a property")
            return redirect('login')

    def get_context_data(self,*args, **kwargs):
        """
        Initialize the data to be sent to the HTML page
        :return: context to be used by the Django Template
        """
        current_property = Property.objects.get(pk=self.get_object().id)
        context = super(UpdateProperty, self).get_context_data(**kwargs)
        context['cities'] = ['New Delhi', 'Noida', 'Gurugram', 'Chandigarh', 'Bangalore', 'Pune', 'Mumbai', 'Chennai']
        context['states'] = ['Delhi', 'Uttar Pradesh', 'Haryana', 'Punjab', 'Karnataka', 'Maharashtra', 'Tamil Nadu']
        context['property_images'] = PropertyImages.objects.filter(property_name=current_property)
        return context

    def form_valid(self, form):
        """
        If the form data is valid, update the property
        :param form: from the template
        :return: on successful updation redirects to dashboard
        """
        form.instance.property_city = form.data['select_city']
        form.instance.property_state = form.data['select_state']
        form.instance.save()
        current_property = Property.objects.get(pk=self.get_object().id)
        if self.request.FILES:
            images = self.request.FILES.getlist('images')
            for image in images:
                current_image = PropertyImages.objects.filter(property_name=current_property)[images.index(image)]
                current_image.property_image = image
                current_image.save()
        return redirect('dashboard')

    def form_invalid(self, form, *args, **kwargs):
        """
        :param form:
        :return: an HttpResponse to a page listing the error
        """
        context = self.get_context_data()
        return render(self.request, self.template_name, context=context)


class DeleteProperty(DeleteView):
    model = Property
    template_name = 'property_delete.html'
    success_url = reverse_lazy('dashboard')

    def get(self, request, *args, **kwargs):

        if self.request.session.get('logged_in', False):

            current_property = Property.objects.get(pk=self.get_object().id)
            current_user = User.objects.get(username=self.request.session.get('current_user'))
            if current_property.property_owner == current_user:
                return super().get(request, *args, **kwargs)
            else:
                logout(self.request)
                messages.add_message(self.request, messages.INFO, "Please login as appropriate seller to post a property")
                return redirect('login')
        else:
            messages.add_message(self.request, messages.INFO,
                                 "Not Logged In, Please login as seller to update a property")
            return redirect('login')


def search(request):
    property_list = Property.objects.all()
    property_filter = PropertyFilter(request.GET, queryset=property_list)
    prop_images = []
    prop = property_filter.queryset
    # prop_images = [PropertyImages.objects.filter(property_name=props) for props in prop]
    for props in prop:
        image = PropertyImages.objects.filter(property_name=props)[0]
        prop_images.append(image)
    final_result = zip(property_filter.qs, prop_images)
    print(property_filter)
    # import pdb; pdb.set_trace()
    return render(request, 'property_search.html', {'filter': property_filter, 'final': final_result})


def handle_query(request, current_property, current_user, id):

    new_enquiry = Enquiry()
    new_enquiry.requester = current_user
    new_enquiry.property = current_property
    new_enquiry.enquiry_text = request.POST.get('query')
    new_enquiry.save()
    return redirect('existing_property', id=id)


def featured_page(request):
    """
    Finds the top 3 properties from Property and send them to display
    :param request:
    :return: top 3 properties to display on the featured page
    """

    prop = []
    prop_images = []
    count = len(Property.objects.filter())
    indexes = [i for i in range(count, count-3, -1)]
    current_user = request.session.get('current_user', None)
    user_name = ''
    if current_user is not None:
        user_name = User.objects.get(username=current_user).first_name
    for i in indexes:
        prop.append(Property.objects.get(pk=i))
        image = PropertyImages.objects.filter(property_name_id=prop[len(prop)-1].id)[0]
        prop_images.append(image)
    final_prop = zip(prop, prop_images)
    return render(request, 'property_featured.html', {'property': prop,
                                                      'property_images': prop_images,
                                                      'range': range(1, 4),
                                                      'final_property': final_prop,
                                                      'logged_in': request.session.get('logged_in', None),
                                                      'user_first_name': user_name,
                                                      'is_seller': request.session.get('is_seller', False)
                                                     })

