from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page

from.views import *


urlpatterns = [
    path('', ServiceIndex.as_view(), name='home'),
    path('about/', About, name='about'),
    path('addpage/', AddService.as_view(), name='create'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('service/<slug:service_slug>/', ShowService.as_view(), name='service'),
    path('category/<slug:cat_slug>/', ServiceCategory.as_view(), name='category'),

]



