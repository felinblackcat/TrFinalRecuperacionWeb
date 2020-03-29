from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from Recomendacion.models import Televisorbb
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as do_logout
from django_pandas.io import read_frame
from matplotlib.backends.backend_agg import FigureCanvasAgg
import matplotlib.pyplot as plt
import io


from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter


@csrf_exempt
def ListarTelevisores(request):
    return render(request,'ListarTelevisores.html')


@csrf_exempt
def EstadisticasTelevisores(request):
    
    qs = Televisorbb.objects.all()
    df = read_frame(qs)    
    
    #Estadisticas:
    
    #Calificacion =  df['calificacion'].describe()  
    
    
    Marca =  df.groupby(['marca'])['marca'].count()
    keys = Marca.keys()
    valores =list(Marca)
    fig = plt.figure(u'MARCA') # Figure
    ax = fig.add_subplot(111) # Axes
    xx = range(len(valores))
    ax.bar(xx, valores, width=0.8, align='center')
    ax.set_xticks(xx)
    ax.set_xticklabels(keys)
    ax.set_title("Marca")
    ax.plot()
    buf = io.BytesIO()
    canvas = FigureCanvasAgg(fig)
    canvas.print_png(buf)
    buf.getvalue()
    fig.clear()
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    TamanoPantalla =  df.groupby(['tamanopantalla']).agg({'tamanopantalla':'count'})
    ETP = TamanoPantalla.describe()
    
    
    
    
    
    TipoPantalla =  df.groupby(['tipodisplay']).agg({'tipodisplay':'count'})
    EtipoP = TipoPantalla.describe()
    
    
    
    Resolucion =  df.groupby(['resolucion']).agg({'resolucion':'count'})
    ER  = Resolucion.describe()
    
    
    JEstadisticas = {'marca':'datos','TamanoPantalla':'datos','TipoPantalla':'datos','Resolucion':'datos','Precio':'datos','Calificacion':'datos'}
    
    
    
    
    
    #
    
    
    
    context = {
                 'Estadisticas':buf.getvalue(),                    
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
            if(user.is_superuser):
                
                return redirect('AdminPanel')
            
            else:
                return redirect('userPanel')
        else:
            
            return redirect('login')
        
        
        
         
        
        

    
    
    
    
    
    
    return render(request,'registro.html')