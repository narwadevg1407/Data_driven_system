from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Files, Folders
from django.contrib import messages
from urllib.parse import urlencode
from django.contrib.auth.models import User


@login_required(login_url="/")
def home(request):
    print("url: ", request.path)
    user_id = request.user.id
    folders = Folders.objects.filter(parent=None,  user_id=user_id)
    files = Files.objects.filter(folder=None, user_id=user_id)

    if request.method == "POST":
        folder_name = request.POST.get("folder_name", None)
        create_folder(request, folder_name=folder_name, user_id=user_id)
    context = {"folders":folders, "files":files}
    return render(request, "app/index.html", context)


@login_required(login_url="/")
def get_folders(request, folder_id):
    user_id = request.user.id
    parent_folders = Folders.objects.filter(id=folder_id)

    if request.method == "POST":
        folder_name = request.POST.get("folder_name", None)
        create_folder(request, folder_name=folder_name,
                      parent_folder_id=folder_id,
                      user_id=user_id)


    folders = Folders.objects.filter(parent_id=folder_id)
    files = Files.objects.filter(folder_id=folder_id)

    context = {"folders":folders, "files":files, "folder_id":folder_id, "path":parent_folders.first()}

    return render(request, "app/index.html", context)


def create_folder(request, folder_name, user_id, parent_folder_id=None):
    user = User.objects.get(id=user_id)
    if not folder_name:
        return
    if not parent_folder_id:
        Folders.objects.create(folder_name=folder_name, user_id=user)
        messages.success(request, "Folder created successfully.")
        return

    parent = Folders.objects.get(id=parent_folder_id) if parent_folder_id else None

    new_folder = Folders(folder_name=folder_name,user_id=user, parent=parent)
    new_folder.save()

    messages.success(request, "Folder created successfully.")


@login_required(login_url="/")
def upload_file(request):
    if request.method == "POST":
        file_name = request.POST.get("file_name", None)
        folder_id = request.POST.get("folder_id")
        file = request.FILES.get("file")
        user_id = request.user.id
        user = User.objects.get(id=user_id)


        if file_name:
            new_file = Files(folder_id=folder_id, user_id=user, file=file, file_name=file_name)
            new_file.save()
            messages.success(request, "File uploaded successfully.")

            return redirect("home")
    return redirect("home")


def get_file_by_id(file_id):
    return Files.objects.filter(id=file_id)


@login_required(login_url="/")
def file_access(request, id):
    files = get_file_by_id(file_id=id)
    if not files:
        return render(request, "app/index.html", {"error":"not such file"})

    context = {"files": files, "is_file_shared": True}
    return render(request, "app/index.html", context)


@login_required(login_url="/")
def delete_file(request, id):
    file = Files.objects.get(id=id)
    file.delete()
    messages.success(request, "File deleted successfully.")

    return redirect("home")


@login_required(login_url="/")
def delete_folder(request, id):
    folder = Folders.objects.get(id=id)
    folder.delete()
    messages.success(request, "Folder deleted successfully.")
    return redirect("home")