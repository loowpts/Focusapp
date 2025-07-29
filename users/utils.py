from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse

def send_activation_email(user, request):
    token = default_token_generator.make_token(user)
    activation_link = request.build_absolute_uri(
        reverse('users:activate', kwargs={'username': user.username, 'token': token})
    )
    subject = 'Подтверждение регистрации'
    message = f"Привет, {user.username}!\n\nПерейдите по ссылке для активации аккаунта:\n{activation_link}"
    send_mail(subject, message, None, [user.email])
