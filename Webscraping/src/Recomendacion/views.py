from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets

# Create your views here.





@csrf_exempt
def index (request):
    
    return render(request,'index.html')

         
  
@csrf_exempt   
def registro(request):      
    return render(request,'registro.html')


@csrf_exempt    
def RegistrarUsuario(request):
    print(request.POST.get('email'),request.POST.get('password'))
    
    context = {
                'mensaje':{'usuario':request.POST.get('email')},
                }
    
    return render(request,'index.html',context)        
 
 