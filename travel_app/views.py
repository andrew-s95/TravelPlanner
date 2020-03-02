from django.shortcuts import render, HttpResponse, redirect
from .models import User, Trip
from time import strftime, strptime
from django.contrib import messages
import datetime
import bcrypt

def homepage(request):
    return render(request, "homepage.html")

def register_page(request):
    if "user_id" in request.session:
        return redirect("/")
    return render(request, "register.html")

def login_page(request):
    if "user_id" in request.session:
        return redirect("/")
    return render(request, "login.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/register")
    else:
        password = request.POST["pw"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        new_user = User.objects.create(first_name = request.POST["fname"], last_name = request.POST["lname"], email = request.POST["email"], pw = pw_hash)
        request.session["user_id"] = new_user.id
        return redirect("/dashboard")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/dashboard")
    else:
        user = User.objects.filter(email = request.POST["email"])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST["pw"].encode(), logged_user.pw.encode()):
                request.session["user_id"] = logged_user.id
                return redirect("/dashboard")
            return redirect("/login")

def dashboard(request):
    if "user_id" not in request.session:
        messages.error(request, "You are no longer logged in")
        return redirect("/login")
    else:
        context = {
            "all_trips": Trip.objects.all(),
            "user_id": User.objects.get(id=request.session["user_id"])
        }
        return render(request, "dashboard.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")

def add_trip_page(request):
    if "user_id" not in request.session:
        messages.error(request, "Not logged in")
        return redirect("/login")
    else:
        context = {
            "user_id": User.objects.get(id=request.session["user_id"])
        }
        return render(request, "addtrip.html", context)

def add_trip(request):
    errors = User.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/trip/add")
    else:
        user = User.objects.get(id = request.session["user_id"])
        dest = request.POST["destination"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        plan = request.POST["plan"]
        Trip.objects.create(user = user, destination = dest, start_date = start_date, end_date = end_date, plan = plan)
        messages.success(request, "Successfully added new trip!")
        return redirect("/dashboard")

def edit_trip_page(request, num):
    if "user_id" not in request.session:
        messages.error(request, "Not logged in")
        return redirect("/login")
    else:
        context = {
            "user_id": User.objects.get(id = request.session["user_id"]),
            "trip": Trip.objects.get(id = num)
        }
        return render(request, "edit.html", context)

def edit_trip(request, num):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/trip/edit/{num}")
    else:
        update_trip = Trip.objects.get(id = num)
        update_trip.destination = request.POST["destination"]
        update_trip.start_date = request.POST["start_date"]
        update_trip.end_date = request.POST["end_date"]
        update_trip.plan = request.POST["plan"]
        update_trip.save()
        messages.success(request, "Successfully editted your trip!")
        return redirect("/dashboard")

def trip_info_page(request, num):
    if "user_id" not in request.session:
        messages.error(request, "Not logged in")
        return redirect("/login")
    else:
        context={
            "user_id": User.objects.get(id=request.session["user_id"]),
            "trip": Trip.objects.get(id=num)
        }
        return render(request, 'trip_info.html', context)

def delete_trip(request, num):
    if "user_id" not in request.session:
        messages.error(request, "Not logged in")
        return redirect('/login')
    trip = Trip.objects.get(id = num)
    if request.session['user_id'] != trip.user.id:
        messages.error(request, "You didn't make this")
        return redirect('/')
    else:
        trip = Trip.objects.get(id = num)
        trip.delete()
        return redirect("/dashboard")



