from django.contrib import auth, messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, View

from account.forms import EmployerRegistrationForm, EmployeeRegistrationForm, UserLoginForm


class UserLoginView(LoginView):
  
    form_class = UserLoginForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        if next_url:
            return next_url
        return reverse('jobapp:dashboard')


class UserLogoutView(View):

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'Has cerrado sesión correctamente.')
        return redirect(reverse_lazy('account:login'))

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


class EmployeeRegistrationView(CreateView):
    form_class = EmployeeRegistrationForm
    template_name = 'account/employee-registration.html'
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Tu cuenta fue creada exitosamente! Por favor, inicia sesión.')
        return redirect(self.success_url)


class EmployerRegistrationView(CreateView):
    form_class = EmployerRegistrationForm
    template_name = 'account/employer-registration.html'
    success_url = reverse_lazy('account:login')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Tu cuenta fue creada exitosamente! Por favor, inicia sesión.')
        return redirect(self.success_url)



