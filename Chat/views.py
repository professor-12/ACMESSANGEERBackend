from django.contrib.auth.models import User
from .serializers import UserSerialiser, ProfileSerializer, ContactSerializer, ChatSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .models import *
from django.db.models import Q
from rest_framework import status
from .pusher import pusher_client


@api_view(["POST"])
def Signup(req):
    serializedData = UserSerialiser(data=req.data)
    if serializedData.is_valid():
        serializedData.save()
        user = User.objects.get(username=req.data["username"])
        user.set_password(req.data["password"])
        user.save()
        profileData = {
            "displayname": user.username,
            "user": user.pk,
            "email": "",
            "user_profile": req.data["username"],
        }
        profile = ProfileSerializer(data=profileData)
        if profile.is_valid():
            profile.save()
        token = Token.objects.create(user=user)
        response = {"token": token.key, "user": serializedData.data}
        return Response(response)
    return Response({"error": serializedData.errors})


@api_view(["POST"])
def Login(req):
    user = get_object_or_404(User, username=req.data["username"])
    if not user.check_password(req.data["password"]):
        return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializedData = UserSerialiser(instance=user, many=False)
    response = {"token": token.key, "user": serializedData.data}
    return Response(response)


@api_view(["GET"])
def Users(req):
    user = Profile.objects.all()
    userserializer = ProfileSerializer(user, many=True)
    return Response(userserializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def POSTChatApi(req):
    if req.method == "POST":
        req.data["sender"] = get_object_or_404(
            User, username=req.user.username).id
        serializedData = ChatSerializer(data=req.data)

        if serializedData.is_valid():
            serializedData.save()
            message = Chat.objects.filter(Q(sender=req.data["sender"], reciever=req.data["reciever"]) | Q(
                sender=req.data["reciever"], reciever=req.data["sender"])).order_by('date')
            const = ChatSerializer(message, many=True)
            pusher_client.trigger(u'chat', u'message',
                                  const.data)
            return Response(serializedData.data)
        return Response(serializedData.errors)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def GETChatApi(req):
    if req.method == "POST":
        sender = get_object_or_404(User, username=req.user.username)
        reciever = get_object_or_404(User, username=req.data["reciever"])
        profile = get_object_or_404(Profile, user=reciever)
        message = Chat.objects.filter(Q(sender=sender, reciever=reciever) | Q(
            sender=reciever, reciever=sender)).order_by('date')
        const = ChatSerializer(message, many=True)
        friendprofileserializer = ProfileSerializer(profile)
        return Response({"messageinfo": const.data, "friendprofile": friendprofileserializer.data})


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def ProfileApi(req):
    user = get_object_or_404(User, username=req.user.username)
    Data = get_object_or_404(Profile, user=user)
    Data.email = user.email
    serializedData = ProfileSerializer(Data)
    return Response(serializedData.data)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def ContactApi(req):
    if req.method == "GET":
        profileuserlist = []
        user = get_object_or_404(User, username=req.user.username).id
        contact = Contacts.objects.filter(Q(user=user))
        for i in contact:
            coontactprofile = get_object_or_404(User, username=i.contact)
            print(coontactprofile)
            profile = get_object_or_404(Profile, user=coontactprofile)
            profileuserlist.append(profile)
        profileserializer = ProfileSerializer(profileuserlist, many=True)
        return Response(profileserializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def CreateContact(req):
    user = get_object_or_404(
        User, username=req.user.username).pk
    contact = get_object_or_404(
        User, pk=req.data["contact"])
    usercontact = Contacts.objects.filter(user=user)
    serializecontact = ContactSerializer(usercontact, many=True)
    for i in serializecontact.data:
        print(contact.pk)
        if i["contact"] == contact.pk:
            return Response("User is already your contact")

    Data = {
        "user": user,
        "contact": contact.id
    }
    contactserializers = ContactSerializer(
        data={"user": contact.id, "contact": user})
    contactserializer = ContactSerializer(data=Data)
    if contactserializer.is_valid():

        contactserializer.save()
    if contactserializers.is_valid():
        if Data["user"] != Data["contact"]:
            contactserializers.save()
            return Response("Contact added succesfully")
    return Response(contactserializer.errors)


@api_view(["PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def EditProfile(req):
    user = get_object_or_404(
        User, username=req.user.username)
    profiles = get_object_or_404(Profile, user=user.id)
    profiles.email = req.user.email
    req.data["user"] = user.id
    profile = ProfileSerializer(instance=profiles, data=req.data)
    if profile.is_valid():
        profile.save()
        userprofile = ProfileSerializer(profiles, many=False)
        pusher_client.trigger('chat', 'profile', userprofile.data)
        return Response("Successful")
    return Response(profile.errors)
