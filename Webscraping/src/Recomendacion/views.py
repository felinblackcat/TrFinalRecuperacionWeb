from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib.auth import login, authenticate





@csrf_exempt
def index (request):
    
    return render(request,'index.html')

@csrf_exempt  
def login(request):
    return render(request,'login.html')         
  
@csrf_exempt   
def registro(request):      
    return render(request,'registro.html')


@csrf_exempt    
def RegistrarUsuario(request):
    
    
    if(request.method=="POST"):
        
        try:
            Usuario = User.objects.create_user(request.POST.get('email'),request.POST.get('email'),request.POST.get('password'))
            Usuario.save()
            context = {
                    'mensaje':{'usuario':request.POST.get('email'),'mensaje':'Registrado Correctamente.'},                    
                    }
    
            return render(request,'index.html',context)      
            
            
            
        
        except IntegrityError:
            context = {
                    'mensaje':{'usuario':request.POST.get('email'),'mensaje':'Error usuario ya registrado.'},                    
                    }
    
            return render(request,'index.html',context)      
            
            
          
 
def Loguearse(request):
    user = authenticate(username=username, password=password)
    login(request, user)
    return redirect('home')

    
    
    
    
    
    
    return render(request,'registro.html')