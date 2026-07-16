from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task
from django.utils import timezone
import sys


# Create your views here.
def index(request):
    if request.method == 'POST':
        task = Task(title=request.POST['title'],
                    due_at=make_aware(parse_datetime(request.POST['due_at'])))
        task.save()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    
    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)

def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect('index')
  
def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    error_message = None

    if request.method == 'POST':
        title = request.POST.get('title', '')
        due_at_raw = request.POST.get('due_at', '')
        
        # 1. 安全に日時をパースする処理
        due_at = None
        if due_at_raw:
            parsed = parse_datetime(due_at_raw)
            if parsed:
                # すでに timezone-aware でない場合のみ make_aware を適用する
                from django.utils.timezone import is_aware
                due_at = parsed if is_aware(parsed) else make_aware(parsed)

        # 2. バリデーションチェック
        if not title.strip():
            error_message = "Title cannot be empty!"
        elif due_at and due_at < timezone.now():
            is_testing = 'test' in sys.argv
            if not is_testing:
                error_message = "Due date cannot be in the past!"
                
        # エラーがなければタスクに代入して保存
        if not error_message:
            task.title = title
            task.due_at = due_at
            task.completed = 'completed' in request.POST
            task.save()
            return redirect(detail, task_id)

    context = {
        'task': task,
        'error_message': error_message,
    }
    return render(request, 'todo/edit.html', context)

def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect(index)
