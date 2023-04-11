from django.shortcuts import render, redirect
from django.contrib import messages
from tasks.models import Task
from .models import Subcontractors, Employees, Trades, SubNotes, PrimaryContact, SubTrades
from .forms import AddEmployeeForm, AddSubcontractorForm

def trades(request):
    if request.method == "POST":
        code = request.POST['code']
        name = request.POST['name']
        t = Trades(code=code, name=name)
        t.save()
        messages.success(request, 'Trade Added')
    trade_list = Trades.objects.all()
    count = Task.objects.filter(completed=False).filter(assigned_to=request.user.id).count()
    return render(request, 'subs/trades.html', {'trade_list': trade_list, 'count': count})


def delete_trade(request, pk):
    t= Trades.objects.get(id=pk)
    t.delete()
    messages.success(request, 'Trade Deleted')
    return redirect('trades')
    pass


def subcontractors(request):
    if request.method == "POST":
        form = AddSubcontractorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subcontractor Added')
            return redirect('sub_detail', form.id)
        else:
            print(form.errors)
            messages.error(request, 'Error Adding Sub')
            return redirect('subcontractors')

    form = AddSubcontractorForm()
    sub_list= Subcontractors.objects.all()
    count = Task.objects.filter(completed=False).filter(assigned_to=request.user.id).count()
    employee = []
    for s in sub_list:
        if s.primary_contact:
            e = Employees.objects.get(pk=s.primary_contact)
            employee.append(e)
        else:
            e = ""
            employee.append(e)
    group = zip(sub_list, employee)
    return render(request, 'subs/subcontractors.html', {'count': count, 'form':form, 'group': group})


def sub_detail(request, id):
    form = AddEmployeeForm()
    if request.method == 'POST':
        note = request.POST['note']
        employee = request.user.first_name[0] + request.user.last_name[0]
        n = SubNotes(note=note, employee=employee, sub=Subcontractors.objects.get(pk=id))
        n.save()
        messages.success(request, 'Note Added')

    sub_form = AddSubcontractorForm()
    sub = Subcontractors.objects.get(pk=id)
    emp = Employees.objects.filter(sub=id)
    notes = SubNotes.objects.filter(sub=id).order_by('-time_created')
    count = Task.objects.filter(completed=False).filter(assigned_to=request.user.id).count()
    trade_list = Trades.objects.all()

    return render(request, 'subs/sub_detail.html', {'sub': sub, 'emp': emp, 'notes': notes, 'count': count, 'trade_list':trade_list, 'form':form, 'sub_form': sub_form})


def add_employee(request, id):
    if request.method == 'POST':
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.sub = Subcontractors.objects.get(pk=id)
            obj.save()
            messages.success(request, 'Employee Added')
            emp = request.user.first_name[0] + request.user.last_name[0]
            note = 'Added ' + str(request.POST['first_name']) + ' ' + str(request.POST['last_name']) + ' to employee list'
            n = SubNotes(employee=emp, note=note, sub=Subcontractors.objects.get(pk=id))
            n.save()
            return redirect('sub_detail', id)
        else:
            print(form.errors)
            messages.error(request, 'Error with form')
            return redirect('sub_detail', id)
    else:
        messages.error(request, 'Error with request')
        return redirect('sub_detail', id)


def set_primary_employee(request, sub, emp):
    s = Subcontractors.objects.get(pk=sub)
    s.primary_contact = emp
    s.save()
    n = SubNotes(sub=Subcontractors.objects.get(pk=sub), employee=request.user.first_name[0] + request.user.last_name[0], note='Switched primary contact to ' + Employees.objects.get(pk=emp).first_name + ' ' + Employees.objects.get(pk=emp).last_name)
    n.save()
    messages.success(request, 'Primary Contact Updated')
    return redirect('sub_detail', sub)


def add_trade(request, sub):
    if request.method == "POST":
        print(request.POST)
        return redirect('sub_detail', sub)

    return redirect('sub_detail', sub)

def upd_emp(request, sub, emp):
    if request.method == "POST":
        form = AddEmployeeForm(request.POST)
        if form.is_valid():
            e = Employees.object.get(pk=emp).update(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], phone=request.POST['phone'])
            messages.success(request, 'Employee updated')
            return redirect('sub_detail', sub)
        else:
            messages.error(request, form.errors)
            return redirect('sub_detail', sub)

    messages.error(request, 'Please delete using form')
    return redirect('sub_detail', sub)

def upd_sub(request, sub):
    pass