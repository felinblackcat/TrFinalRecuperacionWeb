from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from Recomendacion.models import Televisorbb
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as do_logout
from django_pandas.io import read_frame
import pandas as pd
@csrf_exempt
def ListarTelevisores(request):
    return render(request,'ListarTelevisores.html')


@csrf_exempt
def EstadisticasTelevisores(request):
    
    qs = Televisorbb.objects.all()
    df = read_frame(qs)
    EstadisticasDescriptivas = df.describe()
    Marca = df.groupby(['marca']).agg({'marca':'count'})
    TamanoPantalla =  df.groupby(['tamanopantalla']).agg({'tamanopantalla':'count'})
    ETP = TamanoPantalla.describe()
    TipoPantalla =  df.groupby(['tipodisplay']).agg({'tipodisplay':'count'})
    Resolucion =  df.groupby(['resolucion']).agg({'resolucion':'count'})
    
    print(ETP)
    
    
    #
    
    
    
    context = {
                 'ListaUsuarios':'cosa',                    
                    }
    
    
    
    return render(request,'EstadisticasTelevisores.html', context)


@csrf_exempt
def GestionTelevisores(request):
    return render(request,'GestionTelevisores.html')
@csrf_exempt
def SistemaRecomendacion(request):
    return render(request,'SistemaRecomendacion.html')
@csrf_exempt
def MostrarUSuarios(request):
    Consulta = User.objects.all().values('username','is_superuser')
    context = {
                    'ListaUsuarios':Consulta,                    
                    }
            
    
    return render(request,'MostrarUsuarios.html',context)

@csrf_exempt
def AdminPanel(request):
    return render(request,'adminPanel.html')


@csrf_exempt
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
            Usuario = User.objects.create_user(request.POST.get('email'),request.POST.get('email'),request.POST.get('password'),first_name=request.POST.get('nombre'))
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
            if(user.is_superuser):
                
                return redirect('AdminPanel')
            
            else:
                return redirect('userPanel')
        else:
            
            return redirect('login')
        
        
        
         
        
        

    
    
    
    
    
    
    return render(request,'registro.html')