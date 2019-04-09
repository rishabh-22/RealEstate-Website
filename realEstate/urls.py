"""realEstate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from loginRegister import views
from django.conf.urls.static import static
from django.conf import settings
from properties import views as p_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.NewUser.as_view(), name='register'),
    path('form/', views.index,),
    path('login/', views.check_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/', views.Dashboard.as_view(), name='dashboard'),
    path('property/', p_views.CreateNewProperty.as_view(), name='property_featured'),
    path('property/<int:id>/', p_views.ExistingProperty.as_view(), name='existing_property')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
