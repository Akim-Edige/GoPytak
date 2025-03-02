from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
# from django.utils import timezone
# from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView


from .forms import UserRegistrationForm, UserLoginForm
from .models import User


# Create your views here.

class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Авторизация'
    redirect_authenticated_user = True


class UserRegistrationView(TemplateView):
    template_name = 'users/register_forwarder.html'

class ClientRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Success. Please verify your email address.'
    title = 'Store - Registration'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_customer = True
        self.object.save()
        return super().form_valid(form)


class ExecutorRegistrationView(SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Success. Please verify your email address.'
    title = 'Store - Registration'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.is_executor = True
        self.object.save()
        return super().form_valid(form)