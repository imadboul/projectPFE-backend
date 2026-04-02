from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Client(models.Model):
    ROLES = (
        ('client', 'Client'),
        ('admin','Admin'),
        ('superAdmin','Super Admin')
    )
    
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique= True, db_index=True)
    phonenumber = models.CharField(max_length= 20,null=False)
    name = models.CharField(max_length=254,null=False)
    password = models.CharField(max_length=254,null=False)
    lastname = models.CharField(max_length=254,null=False)
    created_at = models.DateField(auto_now_add=True)
    role = models.CharField(max_length=15,choices=ROLES, default='client')
    email_verified = models.BooleanField(default=False)
    
   
    
    def setpassword(self,raw_password):
        self.password = make_password(raw_password)
    def checkpassword(self, raw_password):
        return check_password(raw_password,self.password)
    def fullname(self):
        return f"{self.lastname} ({self.name})"
    
    def changerole(self,role):
        if role in self.ROLES:
            self.role = role
    
    def __str__(self):
        return f"{self.email} ({self.role})"
    
    
class Notification(models.Model):  

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Client,on_delete= models.CASCADE,related_name='notifications')
    title = models.CharField(max_length=254)
    content = models.TextField()
    viewed = models.BooleanField(default= False)
    link = models.TextField()
    
    
