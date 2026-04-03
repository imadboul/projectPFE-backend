from rest_framework import serializers
from .models import *
from django.utils import timezone

class producttypeserializer(serializers.ModelSerializer):
    id = serializers.IntegerField() 
    
    class Meta:
        model = ProductType
        fields = ["id", "name" , "description" ]
        extra_kwargs = {
            "description" : {"read_only": True}
            }
        
    def validate(self, data):
        try:
              type = ProductType.objects.get(id = data.get('id'))
        except ProductType.DoesNotExist:
            raise serializers.ValidationError("does not exist")
        if data.get('name') != type.name :
            raise serializers.ValidationError("does not exist")
        
        return data
    
    
class productserializer(serializers.ModelSerializer):
    id = serializers.IntegerField() 
    
    class Meta:
        model = Product
        fields = [ "id","name","description","unit_price","qte_left","product_type","active"]
        extra_kwargs = {
            "description" : {"read_only": True},
            "qte_left": {"read_only": True},
            "active" : {"read_only": True},
            "unit_price" : {"read_only": True},
            }
        
    def validate(self, data):
        try:
              type = Product.objects.get(id = data.get('id'))
        except Product.DoesNotExist:
            raise serializers.ValidationError("does not exist")
        if data.get('name') != type.name:
            raise serializers.ValidationError("does not exist")
        
        return data
    
    
class producttypecreateserializer(serializers.ModelSerializer):
    
    class Meta:
        model = ProductType
        fields = '__all__'
    
        
    def validate(self, data):
        
        type = ProductType.objects.filter(name = data.get('name')).exists()
       
            
        if type :
            raise serializers.ValidationError("already exists ")
        
        return data
    
    
class productcreateserializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'
        
    def validate(self, data):
        type = Product.objects.filter(name = data.get('name')).exists()
       
            
        if type :
            raise serializers.ValidationError("already exists exist")
        
        return data
    
    
class contractcreateserializer(serializers.ModelSerializer):
    
    class Meta:
        model = Contract
        fields = '__all__'
        extra_kwargs = {
         "qte_used": {"read_only": True},
         "created_at": {"read_only": True},
         "validated_at": {"read_only": True},
         "state": {"read_only": True},
         "validated_by": {"read_only": True},
}
    
    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        
        if  start_date >= end_date:
            raise serializers.ValidationError({
                "end_date": "End date must be after start date"
            })
        
        
        qte_global = data.get('qte_global')
        if qte_global <= 0:
            raise serializers.ValidationError({
                "qte_global": "Quantity must be greater than 0"
            })
        
        return data
    

    def validate_start_date(self, value):
        from datetime import date
        if value < timezone.now():
            raise serializers.ValidationError("Start date cannot be in the past")
        return value
    
    def validate_end_date(self, value):
        from datetime import date
        if value < timezone.now():
            raise serializers.ValidationError("End date cannot be in the past")
        return value
        


class contractserializer(serializers.Serializer):
    
    id = serializers.IntegerField() 
    
    state = serializers.CharField()
    
    def validate_state(self, value):
        STATES = ["pending","validated","rejected"]
        if not value in STATES:
            raise serializers.ValidationError("state does not exist ")
        return value
            

    def validate(self, data):
        try:
              type = Contract.objects.get(id = data.get('id'))
        except Contract.DoesNotExist:
            raise serializers.ValidationError("does not exist")
        return data
    


        
        
        
    

        
        
            
            