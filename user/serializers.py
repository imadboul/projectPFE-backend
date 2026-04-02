from rest_framework import serializers
from .models import *

class ClientSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    
    class Meta:
        model = Client
        fields = ["email", "phonenumber", "name", "lastname", "password"]
        
    def create(self, validated_data):
        password = validated_data.pop("password")
        clienttocreate = Client.objects.model(**validated_data)
        clienttocreate.setpassword(password)
        clienttocreate.save()
        
        return clienttocreate
    
class notificationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification
        fields = ["title", "content", "viewed", "link"]
        

class loginSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only= True)
    
    def validate(self , data):
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = Client.objects.get(email = email)
        except Client.DoesNotExist:
             raise serializers.ValidationError("User not found")
        
        if not user.checkpassword(password):
            raise serializers.ValidationError("Incorrect password")
        if not user.email_verified:
            raise serializers.ValidationError("Email not verified")
        
        data['user'] = user
        
        return user
            
        