from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from django.shortcuts import get_object_or_404
from .models import *
# Create your views here.


def railway_staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            # Redirect to a specific page after successful login
            return redirect('railway_staff_dashboard')  # Replace with your dashboard URL name
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'railway_staff/railway_staff_login.html')  # Render the login form

@login_required
def railway_staff_dash(request):
    return render(request, 'railway_staff/railway_staff_dash.html')


@login_required
def add_trains(request):
    if request.method == 'POST':
        form = TrainForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('railway_staff_dashboard')  # Redirect to a success page after saving the train
    else:
        form = TrainForm()

    return render(request, 'railway_staff/add_train.html', {'form': form})


@login_required
def train_schedules(request):
    running_trains = TrainSchedule.objects.all()
    return render(request, 'railway_staff/train_schedules.html', {
        'running_trains': running_trains,
    })


@login_required
def update_trains(request):
    trains = Train.objects.all()  # Retrieve all trains
    show_form = False
    selected_train = None
    form = None

    if request.method == 'GET':
        train_id = request.GET.get('train_id')
        if train_id:
            selected_train = get_object_or_404(Train, pk=train_id)
            form = TrainForm(instance=selected_train)
            show_form = True

    if request.method == 'POST':
        train_id = request.POST.get('train_id')
        selected_train = get_object_or_404(Train, pk=train_id)
        if 'action' in request.POST:
            if request.POST['action'] == 'button1':
                form = TrainForm(request.POST, instance=selected_train)
                if form.is_valid():
                    form.save()
                    return redirect('update_trains')  # Redirect to a success page after updating the train
            elif request.POST['action'] == 'button2':
                selected_train.delete()
                return redirect('update_trains')

    return render(request, 'railway_staff/update_trains.html', {
        'trains': trains,
        'show_form': show_form,
        'selected_train': selected_train,
        'form': form,
    })
