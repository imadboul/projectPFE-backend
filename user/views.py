from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .serializers import *
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from .models import Client, Notification
from django.core import signing
from rest_framework.renderers import JSONRenderer
from .auth import create_jwt ,decode_jwt
import json



def generatetoken(client : Client):
    data = {'client_id' : client.id}
    token = signing.dumps(data, salt="email-verification")
    
    return token

def verify_token(token):
    try:
        data = signing.loads(token,salt="email-verification")
        return data['client_id']
    except signing.BadSignature:
        return None







@api_view(['POST'])
def signup(request):
    
    
    
    serializer = ClientSerializer(data = request.data)
    
    if serializer.is_valid():
        
        user : Client = serializer.save() # type: ignore
        email = user.email
        
        token = generatetoken(user)
        
        verify_link = f"http://localhost:8000/client/verifyEmail/{token}/"
        
        send_mail(
            'verify email',
            f' click here {verify_link}',
           settings.EMAIL_HOST_USER,
            [email]
            )

        return Response({
            "message": "Account created successfully! (check email)",
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])

def login(request):
    
    serializer = loginSerializer(data = request.data)
    
    if serializer.is_valid():
        client = serializer.validated_data
        
        access, refresh = create_jwt(client) # type: ignore
        
      
        
        return Response(
            {
                "message": "login successful",
                "refresh":refresh,
                "access": access
                
            } , status= status.HTTP_200_OK
        )
    
    return Response({"error" :serializer.errors}, status= status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def verifyEmail(request,token):
    
    user_id = verify_token(token)
    
    if not user_id:
        return Response({"error" :"invalid token"}, status= status.HTTP_400_BAD_REQUEST)
    
    user = get_object_or_404(Client, id = user_id)
    
    user.email_verified = True
    user.save()
    return Response({'message': 'Email verified (go to login)'})
    
    
    
@api_view(["POST"])
def refresh_access(request):
    
    serializer = RefreshTokenserializer(data = request.data )
    
    if not serializer.is_valid():
        return JsonResponse({"error": serializer.error_messages }, status=401)
    
    payload = serializer.validated_data['payload'] # type: ignore
    
    user = Client.objects.get(id = payload.get("user_id")) 
    
    access_token,_ = create_jwt(user)
    
    return JsonResponse({"access_token": access_token})
    
    
def notify_all_superadmin(title,content,link):
    
    superadmins = Client.objects.filter(role = 'superAdmin')
    for admin in superadmins:
        notification = Notification.objects.create(
            user=admin,
            title=title,
            content=content,
            link=link,
            viewed=False  
        )
        
def notify_all_admin(title,content,link):
    
    admins = Client.objects.filter(role__in =['admin', 'superAdmin'])
    for admin in admins:
        notification = Notification.objects.create(
            user=admin,
            title=title,
            content=content,
            link=link,
            viewed=False  
        )
def notify_all_client(title,content,link):
    
    clients = Client.objects.filter(role = 'client')
    for client in clients:
        notification = Notification.objects.create(
            user=client,
            title=title,
            content=content,
            link=link,
            viewed=False  
        )
        
def notify_a_client(id,title,content,link):
    
    client = get_object_or_404(Client, id= id)
    notification = Notification.objects.create(
            user=client,
            title=title,
            content=content,
            link=link,
            viewed=False  
        )
    
    
    
        
    



        




