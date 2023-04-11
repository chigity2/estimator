from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Projects, Architects, ArchitectsContacts, Owners, OwnersContacts, ProjectNotes, Bids
from subs.models import Subcontractors, Trades, SubTrades
from tasks.models import Task

# Create your views here.
def projects(request):
    if request.method == "POST":
        name = request.POST['name']
        number = request.POST['number']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        units = request.POST['units']
        state_pw = request.POST.get('state_pw', False)
        # state_pw = request.POST['state_pw']
        davis_bacon = request.POST.get('davis_bacon', False)
        # davis_bacon = request.POST['davis_bacon']
        p = Projects(name=name, number=number, address=address, city=city, state=state, zip=zip, units=units, state_pw=state_pw, davis_bacon=davis_bacon)
        p.save()
        messages.success(request, 'Project Added')
        return redirect('projects')

    tasks = Task.objects.filter(completed=False).filter(assigned_to=request.user.id)
    count = tasks.count()
    owners = Owners.objects.all().order_by('name')
    projects = Projects.objects.filter(active=True).order_by('-number')

    return render(request, 'projects/projects.html', {'projects': projects, 'owners': owners, 'count': count})


def project_detail(request, id):
    if request.method == "POST":
        name = request.POST['name']
        number = request.POST['number']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        units = request.POST['units']
        owner = request.POST['owner']
        state_pw = request.POST.get('state_pw', False)
        davis_bacon = request.POST.get('davis_bacon', False)
        p = Projects(name=name, number=number, address=address, city=city, state=state, zip=zip, units=units,
                     state_pw=state_pw, davis_bacon=davis_bacon, owner=Owners.objects.get(id=owner))
        p.save()
        n = ProjectNotes(note='Project added', employee=request.user.username()[0:1], project=Projects.objects.get(pk=Projects.objects.all()[0]))
        n.save()
        messages.success(request, 'Project Added')
        return redirect('projects')

    bids = Bids.objects.filter(project=Projects.objects.get(pk=id))
    project_info = Projects.objects.get(pk=id)
    notes = ProjectNotes.objects.filter(project=id).order_by('-date_added')
    owners = Owners.objects.all().order_by('name')
    tasks = Task.objects.filter(completed=False).filter(assigned_to=request.user.id)
    count = tasks.count()
    return render(request, 'projects/project_detail.html', {'project_info': project_info, 'owners': owners, 'notes': notes, 'bids': bids, 'count': count})


def owners(request):
    if request.method == "POST":
        name = request.POST['name']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        o = Owners(name=name, address=address, city=city, state=state, zip=zip)
        o.save()
        return redirect('owners')

    owners_list = Owners.objects.all().order_by('name')
    tasks = Task.objects.filter(completed=False).filter(assigned_to=request.user.id)
    count = tasks.count()
    return render(request, 'projects/owners.html', {'owners': owners_list, 'count': count})


def update_project(request, id):
    if request.method == "POST":
        p = Projects.objects.get(pk=id)
        p.name = request.POST['name']
        p.number = request.POST['number']
        p.address = request.POST['address']
        p.city = request.POST['city']
        p.state = request.POST['state']
        p.zip = request.POST['zip']
        p.units = request.POST['units']
        p.owner = Owners.objects.get(id=request.POST['owner'])
        p.state_pw = request.POST.get('state_pw', False)
        p.davis_bacon = request.POST.get('davis_bacon', False)
        p.save()
        messages.success(request, "updated Successfully")
        return redirect('project_detail', id)


def note(request, id):
    if request.method == "POST":
        note = request.POST['note']
        employee = request.user.username[0:2]
        project = id
        n = ProjectNotes(note=note, employee=employee, project=Projects.objects.get(pk=id))
        n.save()
        messages.success(request, 'Note added')
        return redirect('project_detail', id)

    return redirect('projects')


def add_bid(request, id):
    if request.method == "POST":
        bid_number = request.POST['bid_number']
        plans = request.POST['plans']
        date_due = request.POST['date_due']
        project = Projects.objects.get(pk=id)
        b = Bids(project=project, bid_number=bid_number, plans=plans, date_due=date_due, status='Active')
        b.save()
        messages.success(request, 'New Bid Added')
        return redirect('project_detail', id)


def bid_detail(request, project, id):
    if request.method == "POST":
        pass

    trades = Trades.objects.all()
    subs = SubTrades.objects.all()
    bid_info = Bids.objects.get(pk=id)
    tasks = Task.objects.filter(completed=False).filter(assigned_to=request.user.id)
    count = tasks.count()
    return render(request, 'projects/bid_detail.html', {'bid_info': bid_info, 'trades': trades, 'subs': subs, 'count': count})