from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as do_logout

def userPanel(request):
    return render(request,'userPanel.html')


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
        #(user,email,pass)
        try:
            Usuario = User.objects.create_user(request.POST.get('nombre'),request.POST.get('email'),request.POST.get('password'))
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
            
def deslog(request):
    do_logout(request)
    
    
    return redirect('login')
          
 
def Loguearse(request):
    
    
    if(request.method=="POST"):
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        
        
        if user is not None:
            
            auth_login(request, user)
            return redirect('userPanel')
        else:
            
            return redirect('login')
        
        
        
         
        
        

    
    
    
    
    
    
    return render(request,'registro.html')