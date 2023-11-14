from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Chat(models.Model):
    message = models.TextField(max_length=99999999999999999999999999999)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender")
    reciever = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reciever")
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    time = models.TimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.sender.username


class Contacts(models.Model):
    contact = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="contact", blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")

    def __str__(self):
        return self.user.username


class Profile(models.Model):
    bio = models.CharField(default="A bio", max_length=50)
    profilepics = models.ImageField(upload_to="img/%y", default="default.png")
    email = models.CharField(max_length=100, blank=True)
    location = models.CharField(default="Earth", max_length=20)
    user_profile = models.CharField(max_length=100, default="User_profile")
    displayname = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
