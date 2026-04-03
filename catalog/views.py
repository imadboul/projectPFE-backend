from django.shortcuts import render
from user.wraps import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from .models import *
from django.utils import timezone
from user.views import notify_all_superadmin , notify_a_client







@api_view(['POST', 'GET'])
@jwt_must
def producttype(request):
    if request.method == 'POST':
        
    
        serializer = producttypecreateserializer(data = request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response({
            "message": "Account created successfully! (check email)",
               }, status=status.HTTP_201_CREATED)
        
        else:
            return Response ( { "error" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST )
    
    if request.method == 'GET':
    
        types =  producttypeserializer(ProductType.objects.all() , many = True)
         
        return Response ( { "types" : types.data}, status=status.HTTP_200_OK )


@api_view(['POST','GET'])
@jwt_must
def product(request):
    if request.method == 'POST':
        serializer = productcreateserializer(data = request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response({
               "message": "product created successfully!",
                }, status=status.HTTP_201_CREATED)
        
        else:
            return Response ( { "error" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST )
    
    if request.method == 'GET':
    
        products =  productserializer(Product.objects.filter(active=True),many=True)
         
        return Response ( { "products" : products.data}, status=status.HTTP_200_OK )



@api_view(['POST','GET'])
@jwt_must
def contract(request):
    if request.method == 'POST':
        
    
        serializer = contractcreateserializer(data = request.data)
    
        client_id = request.user_id
    
        if serializer.is_valid():
        
            contract = serializer.save(client_id= client_id)
            notify_all_superadmin('validate contract',f'contract number ({contract.id})','') # type: ignore
            return Response({
                "message": " done wait for validation",
                "contract": contractserializer(contract).data
                   }, status=status.HTTP_201_CREATED)
        
        
        
        else:
            return Response ( { "error" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST )
    
    if request.method == 'GET':
        client_id = request.user_id
        role = request.role
    
        if(role == 'client'):
        
            contracts = contractserializer(Contract.objects.filter(client_id = client_id), many= True)
            return Response ( { "contracts" : contracts.data }, status=status.HTTP_200_OK )
    
        else:
            contracts = contractserializer(Contract.objects.all(), many= True)
            return Response ( { "contracts" : contracts.data }, status=status.HTTP_200_OK )
    
    
    
@api_view(['POST'])
@jwt_must
def validatecontract(request):
    
    serializer = contractserializer(data = request.data)
    
    if serializer.is_valid():
        
        contract = Contract.objects.get(id = serializer.validated_data['id'] )  # type: ignore
        
        contract.state = serializer.validated_data['state'] # type: ignore
        contract.validated_at = timezone.now()
        contract.validated_by_id = request.user_id # type: ignore
        
        contract.save()
        notify_a_client(contract.client_id,'CONTRACT VALIDATED', f'your contract number{ contract.id } has beed validated by a super admin','') # type: ignore
        
        return Response ( { "message" : "contract validated"}, status=status.HTTP_200_OK )
    else:
        return Response ( { "error" : serializer.errors}, status=status.HTTP_400_BAD_REQUEST )
        
         
        
        
    









    
    

        






