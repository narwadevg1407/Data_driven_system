from django.urls import path
from . import views


urlpatterns = [
    path("", views.login_page, name="login_page"),
    path("add-user/", views.add_user, name="add_user"),
    path("add-user/<int:id>/", views.view_user, name="view_user"),
    path("update-user/<int:id>/", views.update_user, name="update_user"),
    path("logout/", views.logout_page, name="logout_page"),
    # path("home/", views.home, name="home"),

]