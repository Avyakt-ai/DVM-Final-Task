from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from railway_staff.models import *
from datetime import datetime, time
from .models import *
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from datetime import timedelta
from django.utils.timezone import make_aware
from django.forms import formset_factory


def type_of_user(request):
    return render(request, 'passengers/type_of_user.html')


def passenger_register(request):
    # When we create a form it is sent as a POST request.
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now login')
            form.save()
            return redirect('passenger_login')
    else:
        form = UserRegisterForm()
    return render(request, 'passengers/register.html', {'form': form})


def passenger_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            # Redirect to a specific page after successful login
            return redirect('passenger_dashboard')  # Replace with your dashboard URL name
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'passengers/passenger_login.html')  # Render the login form


@login_required
def passenger_dash(request):
    return render(request, 'passengers/passenger_dash.html')


@login_required
def search_trains(request):
    # Below is the error message given by book ticket function.
    error_message = request.GET.get('error_message', None)
    # Get all stations to populate the dropdowns
    stations = Station.objects.all()

    # Retrieve form data from the request
    departure_station_id = request.GET.get('departure_station')
    destination_station_id = request.GET.get('destination_station')
    search_date = request.GET.get('date')
    num_of_passengers = request.GET.get('num_of_passengers')

    # If all required form data is provided
    if departure_station_id and destination_station_id and search_date and num_of_passengers:
        # Get stations by their IDs
        departure_station = Station.objects.get(id=departure_station_id)
        destination_station = Station.objects.get(id=destination_station_id)

        # Convert the string date to a datetime object
        search_date = datetime.strptime(search_date, '%Y-%m-%d')

        # Get the day of the week from the provided date
        day_of_week = search_date.strftime('%A').lower()

        # Filter trains based on the given criteria
        available_trains = Train.objects.filter(
            departure_station=departure_station.station_name,
            destination_station=destination_station.station_name,
            **{day_of_week: True}  # Filter by the corresponding day_of_week field
        )
        num_of_passengers = int(request.GET.get('num_of_passengers'))

        if request.method == 'GET':
            # Create an instance of the BookingForm and Passenger info form
            PassengerInformationFormSet = formset_factory(PassengerInformationForm, extra=num_of_passengers)
            formset = PassengerInformationFormSet()
            booking_form = BookingForm()

            # Render the template with the obtained data and the booking form
            return render(request, 'passengers/search_trains.html', {
                'stations': stations,
                'available_trains': available_trains,
                # 'train_schedules': train_schedules,
                'search_date': search_date,
                'dow': day_of_week,
                'booking_form': booking_form,  # Pass the booking form to the template
                'formset': formset,
                'num_of_passengers': num_of_passengers,
            })

    # If form data is incomplete or not provided, render the template with stations only
    return render(request, 'passengers/search_trains.html', {
        'stations': stations,
        'dep': departure_station_id,
        'des': destination_station_id,
        'date': search_date,
        'error_message': error_message,
    })


@login_required
def book_ticket(request):
    if request.method == 'POST':
        # Process the booking form
        booking_form = BookingForm(request.POST)
        # passenger_info_forms = [PassengerInformationForm(request.POST, prefix=str(i)) for i in range(int(request.POST.get('num_of_passengers', 0)))]

        search_date = request.POST.get('date')

        if booking_form.is_valid():
            selected_train_id = request.POST.get('selected_train_id')
            selected_train = Train.objects.get(id=selected_train_id)
            search_date = datetime.strptime(search_date, '%Y-%m-%d')
            seat_type = request.POST.get('seat_type')

            num_of_passengers = int(request.POST.get('num_of_passengers'))

            available_train_schedule = TrainSchedule.objects.filter(
                departure_date=search_date,
                train=selected_train,
            )
            if not available_train_schedule:
                # Creating a TrainSchedule object
                new_train_schedule = TrainSchedule.objects.create(
                    train=selected_train,
                    departure_date=search_date,
                    arrival_date=datetime.today(),
                    available_seats=selected_train.available_seats,
                )
            # Retrieve other passenger details from the form as needed
            if seat_type == 'general':
                total_fare = selected_train.general_fare*num_of_passengers
            elif seat_type == 'sleeper':
                total_fare = selected_train.sleeper_fare*num_of_passengers
            elif seat_type == '3rd AC':
                total_fare = selected_train.third_ac_fare*num_of_passengers
            elif seat_type == '2nd AC':
                total_fare = selected_train.second_ac_fare*num_of_passengers
            elif seat_type == '1st AC':
                total_fare = selected_train.first_ac_fare*num_of_passengers


            passenger_profile = request.user.passengerprofile
            available_train_schedule = TrainSchedule.objects.get(
                departure_date=search_date,
                train=selected_train,
            )
            if num_of_passengers <= available_train_schedule.available_seats and passenger_profile.wallet_balance >= total_fare:
                # Create a new Booking object and save it to the database
                new_booking = Booking.objects.create(
                    train=selected_train,
                    num_of_passengers=num_of_passengers,
                    departure_date=search_date,
                    total_fare=total_fare,
                    passenger=passenger_profile
                    # Add other fields from the form
                )
                available_train_schedule.available_seats -= num_of_passengers
                available_train_schedule.save()

                passenger_profile.wallet_balance -= total_fare
                passenger_profile.save()

                PassengerInformationFormSet = formset_factory(PassengerInformationForm, extra=num_of_passengers)
                formset = PassengerInformationFormSet(request.POST)
                if formset.is_valid():
                    for form in formset:
                        new_passenger_object = PassengerInformation.objects.create(
                            booking=new_booking,
                            passenger_name=form.cleaned_data['passenger_name'],
                            passenger_email=form.cleaned_data['passenger_email'],
                        )
                return redirect('your_bookings')  # Redirect to success page after successful booking
            else:
                if num_of_passengers > available_train_schedule.available_seats and passenger_profile.wallet_balance>=total_fare:
                    error_message = 'Not enough seats available'
                elif passenger_profile.wallet_balance<total_fare and num_of_passengers <= available_train_schedule.available_seats:
                    error_message = 'Insufficient Funds'
                else:
                    error_message = 'Not enough seats and Insufficient Funds'
                return redirect(reverse('search_trains') + f'?error_message={error_message}')

        # If the form is not valid, handle the errors or redirect as needed
        # For example, re-render the search_trains.html template with an error message
        return render(request, 'passengers/search_trains.html', {
            'error_message': 'Booking form is invalid. Please try again.',  # Pass an error message
        })


@login_required
def account_page(request):
    add_money_form = AddMoneyForm()
    if request.method == 'POST':
        add_money_form = AddMoneyForm(request.POST)
        if add_money_form.is_valid():
            amount_to_add = add_money_form.cleaned_data['amount_added']
            user_profile = request.user.passengerprofile
            user_profile.wallet_balance += amount_to_add
            user_profile.save()

            messages.success(request, f'₹{amount_to_add} added to your wallet successfully!')
            # Redirect to the account page or any other relevant page
            return redirect('account_page')
    return render(request, 'passengers/account.html', {
        'add_money_form': add_money_form,
    })


@login_required
def your_bookings_page(request):
    # Retrieve the current logged-in user's PassengerProfile
    passenger_profile = request.user.passengerprofile

    # Fetch past journeys (departures that have already happened)
    past_journeys = Booking.objects.filter(
        passenger=passenger_profile,
        departure_date__lt=timezone.now()
    )

    # Fetch upcoming journeys (departures that are yet to happen)
    upcoming_journeys = Booking.objects.filter(
        passenger=passenger_profile,
        departure_date__gte=timezone.now()
    )
    for journey in upcoming_journeys:
        # Assuming departure_time is a time object
        departure_date = journey.departure_date
        departure_time = journey.train.departure_time
        complete_departure_datetime = datetime.combine(departure_date, departure_time)
        journey.complete_departure_datetime = complete_departure_datetime

    for journey in upcoming_journeys:
        time_diff_hours = (make_aware(journey.complete_departure_datetime) - timezone.now()).total_seconds() / 3600
        journey.time_diff_hours = time_diff_hours

    return render(request, 'passengers/your_bookings.html', {
        'past_journeys': past_journeys,
        'upcoming_journeys': upcoming_journeys,
    })


@login_required
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking_datetime = datetime.combine(booking.departure_date, booking.train.departure_time)
    booking_datetime_aware = make_aware(booking_datetime)  # Making this datetime object same as timezone object.

    # Check if the booking is cancelable (within the allowed time frame)
    time_diff = booking_datetime_aware - timezone.now()
    if time_diff > timedelta(hours=6):
        # Perform cancellation logic here
        user_profile = request.user.passengerprofile
        user_profile.wallet_balance += booking.total_fare
        user_profile.save()
        # For example:
        booking.is_cancelled = True
        booking.save()
        # Add further logic if required

    return redirect('your_bookings')  # Redirect back to the bookings page after cancellation