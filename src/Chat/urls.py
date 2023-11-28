from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.Signup, name="Signup"),
    path("chat", views.POSTChatApi, name="chatApi"),
    path("profile", views.ProfileApi, name="profile"),
    path("users", views.Users, name="users"),
    path("message/", views.GETChatApi, name="getMessage"),
    path("contact/", views.ContactApi, name="contact"),
    path("Login/", views.Login, name="Login"),
    path("contactcreation/", views.CreateContact, name="CreateContact"),
    path("editprofile", views.EditProfile, name="EditProfile"),
]
