import random
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from accounts.forms import RegisterForm
from accounts.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False  # Аккаунт активируется после верификации почты
        user.save()

        # Отправляем письмо с подтверждением
        current_site = get_current_site(self.request)
        mail_subject = 'Подтвердите вашу регистрацию.'
        message = render_to_string('accounts/activate_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(
            mail_subject,
            message,
            'admin@example.com',
            [user.email],
            fail_silently=False,
        )

        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'


class PasswordResetView(FormView):
    template_name = 'accounts/password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        try:
            user = User.objects.get(email=email)

            # Генерируем новый пароль
            new_password = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=8))
            user.set_password(new_password)  # Устанавливаем новый пароль
            user.save()

            # Отправляем новый пароль пользователю
            send_mail(
                'Восстановление пароля',
                f'Ваш новый пароль: {new_password}',
                'admin@example.com',
                [user.email],
                fail_silently=False,
            )
            form.cleaned_data['email'] = ''  # Очищаем поле email после успешной отправки
            form.add_error(None, 'Новый пароль был отправлен на ваш email.')  # Успешное сообщение
        except User.DoesNotExist:
            form.add_error('email', 'Пользователь с таким email не найден')

        return super().form_valid(form)


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
