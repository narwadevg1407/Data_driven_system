from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from app.models import Folders

# Create your views here.


def login_page(request):
    try:
        request.session["login_id"]
        return redirect("all_folders")
    except:
        pass
    if request.method == "POST":
        # breakpoint()
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user != None:
            request.session["login_id"] = request.user.id
            login(request, user)
            return redirect("home")
        else:

            messages.error(request, "Invalid username or password !!!")
            return redirect("/")

    return render(request, "user_access/login.html")


def add_user(request):
    if request.method == "POST":
        u_name = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        new_user = User(username=u_name, email=email)
        new_user.set_password(password)
        new_user.save()

        messages.success(request, "User creates successfully !")
        return redirect("/")

    return render(request, "user_access/addUser.html")


def view_user(request, id):
    user = User.objects.get(id=id)
    return render(request, "user_access/viewUser.html", {"user":user})


def update_user(request, id):
    user = User.objects.get(id=id)

    if request.method == "POST":
        user.username = request.POST.get("username")
        user.email = request.POST.get("email")
        password = request.POST.get("password")

        if password and password.strip():
            user.set_password(password)
            user.save()
            messages.success(request, "User updated successfully.")

            update_session_auth_hash(request, user)

        else:
            user.save()
            messages.success(request, "User updated successfully.")

        return redirect("home")

    context = {"user":user}
    return render(request, "user_access/updateUser.html", context)


def logout_page(request):
    logout(request)
    return redirect("/")



