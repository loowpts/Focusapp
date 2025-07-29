from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import UserForm, UserProfileForm, RegisterForm
from django.contrib import messages
from django.utils.timezone import now as timezone_now
from .models import UserProfile
from main.models import Task
from django.utils import timezone
from django.db.models import Q
from django.db.models import F
from django.db.models.functions import TruncDate
from .utils import send_activation_email
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            send_activation_email(user, request)
            return render(request, 'users/registration/activation_sent.html')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    tasks = Task.objects.filter(user=user)
    now = timezone.now()

    total_tasks = tasks.count()

    done_on_time = tasks.annotate(
        deadline_date=TruncDate('deadline'),
        done_date=TruncDate('updated_at')
    ).filter(
        status='done',
        deadline__isnull=False,
        done_date__lte=F('deadline_date')
    ).count()


    overdue_tasks = tasks.annotate(
        deadline_date=TruncDate('deadline'),
        done_date=TruncDate('updated_at')
    ).filter(
        (
            Q(status='done', done_date__gt=F('deadline_date')) |  
            Q(status__in=['new', 'in_progress'], deadline__lt=timezone_now())
        ),
        deadline__isnull=False
    ).count()

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно сохранён!')
            return redirect('users:profile')
    else:
        user_form = UserForm(instance=user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'date_joined': user.date_joined,
        'last_login': user.last_login,
        'total_tasks': total_tasks,
        'done_on_time': done_on_time,
        'overdue_tasks': overdue_tasks,
        'now': timezone_now(),
    }
    return render(request, 'users/profile.html', context)


def activate_account(request, username, token):
    user = get_object_or_404(User, username=username)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'users/registration/activation_success.html')
    return render(request, 'users/registration/activation_invalid.html')

