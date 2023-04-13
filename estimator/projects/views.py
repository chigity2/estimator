from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Projects, Architects, ArchitectsContacts, Owners, OwnersContacts, ProjectNotes, Bids, Packages, SubPackages
from subs.models import Subcontractors, Trades, SubTrades, SubNotes
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
        project_id = Projects.objects.get(pk=project)
        bid = Bids.objects.get(pk=id)
        trade = Trades.objects.get(pk=request.POST['trade'])
        estimator = User.objects.get(pk=request.POST['estimator'])
        package = Packages(project=project_id, bid=bid, trade=trade, estimator=estimator)
        package.save()
        messages.success(request, 'Bid Package Added')
        return redirect('bid_detail', project, id)
        pass

    trades = Trades.objects.all()
    estimators = User.objects.all()
    subs = SubTrades.objects.all()
    bid_info = Bids.objects.get(pk=id)
    tasks = Task.objects.filter(completed=False).filter(assigned_to=request.user.id)
    count = tasks.count()
    trade_list = Packages.objects.filter(bid=Bids.objects.get(pk=id))
    package_list = []
    for t in trade_list:
        tid = t.id
        tr = t.trade.code + ' ' + t.trade.name
        tc = SubPackages.objects.filter(bid_package=t).count()
        tab = SubPackages.objects.filter(bid_package=t, bidding=True).count()
        trc = SubPackages.objects.filter(bid_package=t, received__isnull=False).count()
        est = t.estimator.first_name + ' ' + t.estimator.last_name
        val = t.value
        package_list.append({'id': tid, 'trade': tr, 'estimator': est, 'invited': tc, 'bidding': tab, 'received': trc, 'value': val})
    return render(request, 'projects/bid_detail.html', {'bid_info': bid_info, 'trades': trades, 'subs': subs, 'count': count, 'estimators': estimators, 'package_list': package_list})


def update_bid(request, project, id):
    if request.method == "POST":
        b = Bids.objects.get(pk=id)
        b.bid_number = request.POST['bid_number']
        b.plans = request.POST['plans']
        b.date_due = request.POST['date_due']
        b.sub_bids_due = request.POST['sub_bids_due']
        b.save()
        messages.success(request, 'Bid Updated')
        return redirect('update_bid', project, id)
        pass

    return redirect('bid_detail', project, id)

def bid_packages(request, project, id, package):
    if request.method == "POST":
        p = Packages.objects.get(pk=package)
        p.estimator = User.objects.get(pk=request.POST['estimator'])
        p.value = request.POST['value']
        p.save()
        messages.success(request, 'Package Updated')
        return redirect('bid_packages', project, id, package)
        pass

    package_info = Packages.objects.get(pk=package)
    estimators = User.objects.all()
    subs = SubTrades.objects.filter(trade=package_info.trade)
    subs_bidding = SubPackages.objects.filter(bid_package=Packages.objects.get(pk=package))
    return render(request, 'projects/package_detail.html', {'package_info': package_info, 'estimators': estimators, 'subs': subs, 'subs_bidding': subs_bidding})


def invite_sub(request, project, id, package):
    if request.method == "POST":
        print('here')
        sub_checks = request.POST.getlist('sub')
        print(sub_checks)
        for s in sub_checks:
            sp = SubPackages(bid_package=Packages.objects.get(pk=package), sub=Subcontractors.objects.get(pk=s))
            sp.save()
        messages.success(request, 'Subs Invited')
        return redirect('bid_packages', project, id, package)
        pass
    pass


def bid_received(request, project, id, package, subpack):
    if request.method == "POST":
        pack = SubPackages.objects.get(pk=subpack)
        pack.received = timezone.now()
        pack.save()
        messages.success(request, 'Bid Received')
        return redirect('bid_packages', project, id, package)
    pass


def upd_bidding(request, project, id, package, subpack):
    if request.method == "POST":
        sp = SubPackages.objects.get(pk=subpack)
        sp.bidding = request.POST['bidding']
        sp.save()
        messages.success(request, 'Updated')
        return redirect('bid_packages', project, id, package)
    pass