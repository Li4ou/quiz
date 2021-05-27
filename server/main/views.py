from main.form import UserForm

from django.views.generic import TemplateView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect, HttpResponse


# Create your views here.


class Main(LoginRequiredMixin, TemplateView):
    login_url = '/login/'
    template_name = 'main.html'


class Login(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'

    def get_redirect_url(self):
        return '/'


class Registration(TemplateView):
    redirect_authenticated_user = True
    template_name = 'registration.html'

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            return redirect('/')
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)

    def get(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        context = self.get_context_data(**kwargs)
        context['form'] = form

        return self.render_to_response(context)


class Logout(LogoutView):
    template_name = 'login.html'
