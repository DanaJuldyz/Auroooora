from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
from .forms import *
from .models import *
from .utils import DataMixin,menu
from django.contrib.auth.mixins import  LoginRequiredMixin



def user_context(title):
    pass


class ServiceIndex(DataMixin,ListView):
    model = Service
    template_name = 'content/index.html'
    context_object_name = 'services'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Main Page")
        return  dict(list(context.items())+list(c_def.items()))


    def get_queryset(self):
        return Service.objects.filter(is_published=True).select_related('cat')



def About(request):
    contact_list = Service.objects.all()
    paginator = Paginator(contact_list,3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'content/about.html',{'page_obj':page_obj,'menu': menu,'title': 'About Site'})

class AddService(LoginRequiredMixin,CreateView,DataMixin):
    form_class = AddServiceForm
    template_name = 'content/create.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="ADD Service")
        return dict(list(context.items())+list(c_def.items()))



class ContactFormView(DataMixin,FormView):
    form_class = ContactForm
    template_name = 'content/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Contact")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self,form):
        print(form.cleaned_data)
        return redirect('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class ShowService(DetailView,DataMixin):
    model = Service
    template_name = 'content/service.html'
    slug_url_kwarg = 'service_slug'
    context_object_name = 'service'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['service'])
        return dict(list(context.items())+list(c_def.items()))


class ServiceCategory(DataMixin, ListView):
    model = Service
    template_name = 'content/index.html'
    context_object_name = 'service'
    allow_empty = False

    def get_queryset(self):
        return Service.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Category - ' + str(c.name),
                                      cat_selected=c.pk)

        return dict(list(context.items())+list(c_def.items()))



class RegisterUser(DataMixin,CreateView):
    form_class = RegisterUserForm
    template_name = 'content/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self,*, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Registration')
        return dict(list(context.items())+list(c_def.items()))

    def form_valid(self,form):
        user = form.save()
        login(self.request,user)
        return redirect('home')



class LoginUser(DataMixin,LoginView):
    form_class = LoginUserForm
    template_name = 'content/login.html'

    def get_context_data(self,*, object_list=None,**kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title ='Autorization')
        return dict(list(context.items())+list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('home')



