from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from datetime import datetime, timedelta, time, date
from .models import Task, Logs
from projects.models import Projects
from django.db.models import Count
from django.db.models.functions import TruncDay

def home(request):
    if request.method == "POST":
        task_name = request.POST['task_name']
        user = request.user.id
        form = Task(task_name=task_name, assigned_to=user)
        form.save()
        messages.success(request, 'Added Successfully')
        return redirect('home')

    if request.method == "GET":
        today = datetime.now().date()
        tomorrow = today + timedelta(1)
        yesterday = today - timedelta(1)
        tasks = Logs.objects.filter(active_task=True, user=request.user.id, task_date__lt=tomorrow)
        categories = tasks.distinct('category').values('category')
        count = tasks.count()
        call_list = Logs.objects.filter(active_task=True, user=request.user.id, type='phone', task_date__lt=tomorrow).order_by('-task_date')
        note_list = Logs.objects.filter(active_task=True, user=request.user.id, type='task', task_date__lt=tomorrow).order_by('-task_date')
        upcoming = Logs.objects.filter(active_task=True, user=request.user.id, task_date__gte=tomorrow).order_by('task_date')
        ph_complete_count = Logs.objects.filter(active_task=False, user=request.user.id, type='phone', completed_date__lt=tomorrow, completed_date__gt=yesterday).count()
        note_complete_count = Logs.objects.filter(active_task=False, user=request.user.id, type='task', completed_date__lt=tomorrow, completed_date__gt=yesterday).count()
        total_count = ph_complete_count + note_complete_count
        projects = Projects.objects.filter(active=True)
        return render(request, 'tasks/home.html', {'projects': projects, 'tasks': tasks, 'count': count, 'call_list': call_list, 'note_list': note_list, 'upcoming': upcoming, 'today': today, 'ph_count': ph_complete_count, 'no_count': note_complete_count, 'tot_count': total_count, 'categories': categories})

def complete(request, id):
    if request.method == "POST":
        task = Task.objects.get(pk=id)
        task.completed = True
        task.save()
        messages.success(request, 'Completed Successfully')
        return redirect('home')
    else:
        messages.error(request, 'Please click button to complete')
        return redirect('home')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged In")
            return redirect('home')
        else:
            messages.error(request, "Error logging in.")

    return redirect('home')

def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect('home')


def logs(request):
    if request.method == "POST":
        task_date = request.POST['task_date']
        type = request.POST['type']
        task = request.POST['task']
        title = request.POST['title']
        category = request.POST['category']
        user = User.objects.get(pk=request.user.id)
        quick_add = request.POST.get('quick_add', False)
        if quick_add:
            completed_date = timezone.now()
            active_task = False
        else:
            completed_date = None
            active_task = True
        l = Logs(task_date=task_date, type=type, task=task, user=user, completed_date=completed_date, active_task=active_task, title=title, category=category)
        l.save()
        messages.success(request, 'Task Added')
        return redirect('home')

    return redirect('home')


def complete_task(request, id):
    if request.method == "POST":
        l = Logs.objects.get(pk=id)
        l.active_task = False
        l.completed_date = timezone.now()
        l.save()
        messages.success(request, 'Completed task!')
        return redirect('home')

    return redirect('home')


def cancel_task(request, id):
    if request.method == "POST":
        l = Logs.objects.get(pk=id)
        l.active_task = False
        l.save()
        messages.success(request, 'Canceled task')
        return redirect('home')

    return redirect('home')

def daily_recap(request):
    if request.method == "POST":
        subject = "Daily Recap"
        today = datetime.now().date()
        two_days_ago = today - timedelta(2)
        yesterday_tasks = Logs.objects.filter(active_task=False, completed_date__lt=today, completed_date__gt=two_days_ago, user=request.user.id)
        y_tasks_count = yesterday_tasks.count()
        ctx = {'user': User.objects.get(pk=request.user.id), 'y_tasks': yesterday_tasks, 'y_count': y_tasks_count}
        message = get_template('tasks/daily_recap.html').render(ctx)
        msg = EmailMessage(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [request.user.email, ],
        )
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()
        print("Mail successfully sent")

        return redirect('home')


def profile(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        user = User.objects.get(pk=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        messages.success(request, 'Updated')
        return redirect('profile')
        pass

    user = User.objects.get(pk=request.user.id)
    len_f = len(user.first_name)
    last_letter = user.first_name[len_f-1]
    if last_letter == 's':
        adder = "'"
    else:
        adder = "'s"
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    last_week = today - timedelta(7)
    tasks_completed = Logs.objects.filter(active_task=False, user=request.user.id, completed_date__lt=tomorrow,
                                          completed_date__gt=last_week).annotate(day=TruncDay('completed_date'))\
        .values('day').annotate(c=Count('id')).values('day', 'c').order_by('day')
    tasks = Logs.objects.filter(active_task=True, user=request.user.id, task_date__lt=tomorrow)
    count = tasks.count()

    return render(request, 'tasks/profile.html', {'user': user, 'logs': logs, 'adder':adder, 'tasks_completed': tasks_completed, 'count': count})