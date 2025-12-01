from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.dateparse import parse_date
from django.views.decorators.http import require_GET
from django.utils import timezone
from .models import Task
from django.urls import reverse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

@require_GET
@login_required
def get_tasks_for_date(request):
    start_str = request.GET.get('start')
    end_str = request.GET.get('end')

    if not start_str or not end_str:
        return JsonResponse({'error': 'Missing start or end date'}, status=400)

    try:
        start_date = datetime.strptime(start_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_str, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)

    today = timezone.localdate()
    tasks = Task.objects.filter(user=request.user, deadline__range=(start_date, end_date))

    data = []
    for task in tasks:
        overdue = task.deadline < today and task.status != 'done'

        data.append({
            'id': task.id,
            'title': task.title,
            'start': task.deadline.isoformat(),  # <-- важно
            'url': reverse('main:task_detail', args=[task.id]),
            'status': task.status,
            'priority': task.priority,
            'overdue': overdue,
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
@login_required
def create_task_api(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date_str = request.POST.get('date')

        if not title or not date_str:
            return JsonResponse({'success': False, 'message': 'Missing title or date'}, status=400)

        date = parse_date(date_str)
        if not date:
            return JsonResponse({'success': False, 'message': 'Invalid date format'}, status=400)

        Task.objects.create(
            user=request.user,
            title=title,
            deadline=date,
            description=request.POST.get('description', ''),
            status='in_progress',
            priority=request.POST.get('priority', 'medium')
        )
        return JsonResponse({'success': True, 'message': 'Task created'})

    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)
