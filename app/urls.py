from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path("", views.home, name="home"),
    path("folders/<int:folder_id>/", views.get_folders, name="folders"),
    path("upload-file/", views.upload_file, name="upload_file"),
    path("file/access/<int:id>/", views.file_access, name="file_access"),
    path("delete-file/<int:id>/", views.delete_file, name="delete_file"),
    path("delete-folder/<int:id>/", views.delete_folder, name="delete_folder"),

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

