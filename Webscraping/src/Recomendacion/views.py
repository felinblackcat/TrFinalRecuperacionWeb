from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from Recomendacion.models import Televisor,Calificacion,Usuario,Precision
from django.db.utils import IntegrityError
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as do_logout
from django_pandas.io import read_frame
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.db.models import Count
import matplotlib.pyplot as plt
import io
import base64
import urllib
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter
import psycopg2
from itertools import chain
from Recomendacion.Recomendacion import recomendacion,perfil_usuario
from django.db.models import Q

@csrf_exempt
def GuardarCalificacion(request):
     if(request.method=="POST"):
         usuario_actual = request.user.username
         
         db_connection= psycopg2.connect(user = "postgres",password = "Felingato1992",host = "127.0.0.1",port = "5432",database = "tvrec")
         cursor = db_connection.cursor()
         
         try:
            
            sql = "INSERT INTO calificacion(correo,modelo,calificacionusuario) values(%s,%s,%s)"
            values = (usuario_actual,request.POST.get('modelo'),request.POST.get('input-1'))
            cursor.execute(sql,values)
            db_connection.commit()
            return redirect('../userPanel/MostrarTelevisores')
         except Exception as error:
            db_connection.rollback()
            sql = "UPDATE calificacion SET calificacionusuario = %s where correo = %s and modelo = %s"
            cursor.execute(sql,(request.POST.get('input-1'),usuario_actual,request.POST.get('modelo')))
            db_connection.commit()
            return redirect('../userPanel/MostrarTelevisores')
        
def CalificarRecomendacion(request):
    if(request.method=="POST"):
        usuario_actual = request.user.username
        db_connection= psycopg2.connect(user = "postgres",password = "Felingato1992",host = "127.0.0.1",port = "5432",database = "tvrec")
        cursor = db_connection.cursor()
        if(request.POST.get('botoni') == "me gusta"):
                
         
            try:
                
                
                sql = "UPDATE Precision SET calificacion = %s where usuario = %s and modelo = %s"
                values = ('True',usuario_actual,request.POST.get('datosboton'))
                
                print(values)
                
                cursor.execute(sql,values)
                print("sigue")
                db_connection.commit()
                print("Hago commit")
                return redirect('../userPanel/VerRecomendaciones')
            except Exception as error:
                print("Excepcion")
                print(error)
                db_connection.rollback()
                return redirect('../userPanel/VerRecomendaciones')
        
        else:
            
            try:
                
                sql = "UPDATE Precision SET calificacion = %s where usuario = %s and modelo = %s"
                values = ("False",usuario_actual,request.POST.get('datosboton'))
                cursor.execute(sql,values)
                db_connection.commit()
                return redirect('../userPanel/VerRecomendaciones')
            except Exception as error:
                db_connection.rollback()
                return redirect('../userPanel/VerRecomendaciones')
                
    

         
             
@csrf_exempt
def MostarCalificaciones(request):
        Query=Calificacion.objects.all().order_by('correo').values()
        print(Query)
        context = {
                        'ListaCalificaiones':Query,                    
                        }
        return render(request,'MostrarCalificaciones.html',context)

@csrf_exempt
def MostrarRecomendaciones(request):
        Query=Precision.objects.all().order_by('modelo').values()
        
        context = {
                        'ListaRecomendaciones':Query,                    
                        }
        return render(request,'MostrarRecomendaciones.html',context)

@csrf_exempt
def MostrarPresicion(request):
    
    
        
    TotalSistema=Precision.objects.all().filter(~Q(calificacion = None)).count()
    
    AcertividadTotal = Precision.objects.all().filter(calificacion ="True").count()           
    
    TotalColaborativo = Precision.objects.all().filter(sistema_recomendacion='Colaborativo').filter(~Q(calificacion = None)).count()

    AcertividadColaborativo = Precision.objects.all().filter(sistema_recomendacion='Colaborativo',calificacion="True").count()
    
    
    TotalContenido = Precision.objects.all().filter(sistema_recomendacion='Contenido').filter(~Q(calificacion = None)).count()
    AcertividadContenido = Precision.objects.all().filter(sistema_recomendacion='Contenido',calificacion="True").count()
    
    
    try:
        PresionTotal = AcertividadTotal/TotalSistema
    except:
        PresionTotal = 0
    try:
        PresisionColaborativo = AcertividadColaborativo/TotalColaborativo
    except:
         PresisionColaborativo = 0
    try:
         PresisionContenido = AcertividadContenido/TotalContenido
    except:
         PresisionContenido = 0        
            
            
           
            
    context = {
                    'Presicion':{"Total":str(round(PresionTotal*100,2))+'%',"Colaborativo":str(round(PresisionColaborativo*100,2))+'%',"Contenido":str(round(PresisionContenido*100,2))+'%'},                    
                    }
    return render(request,'MostrarPresision.html',context)


def MostrarPrecisionUsuario():
    
    
        
    TotalSistema=Precision.objects.all().filter(~Q(calificacion = None)).count()
    
    AcertividadTotal = Precision.objects.all().filter(calificacion ="True").count()           
    

    
    try:
        PresionTotal = AcertividadTotal/TotalSistema
    except:
        PresionTotal = 0
           
            

    return str(round(PresionTotal*100,2))+"%"

###################################################################################################################################
@csrf_exempt
def BuscarTelevisor(request):
    
    print(request.POST.get('busqueda'))
    if(request.POST):
        Query = Televisor.objects.all().filter(modelo=request.POST.get('busqueda'))
        context = {
                        'ListaTelevisores':Query,                    
                        }
        return render(request,'ListarTelevisores.html',context)
    






@csrf_exempt
def ListarTelevisores(request):
    Query = Televisor.objects.all().values()
    Query2 = Televisor.objects.all().filter(calificacion__correo__isnull=True ).values('calificacion') | Televisor.objects.all().filter(calificacion__correo='correo' ).values('calificacion')
    Query3 = Televisor.objects.filter(calificacion__correo__isnull=True ).values('calificacion__calificacionusuario','modelo','observaciones','marca','precio','tamanopantalla','resolucion','tipodisplay','urlwalmart','urlbb')| Televisor.objects.all().filter(calificacion__correo='correo' ).values('calificacion__calificacionusuario','modelo','observaciones','marca','precio','tamanopantalla','resolucion','tipodisplay','urlwalmart','urlbb')
    
    context = {
                    'ListaTelevisores':Query,                    
                    }
            
    return render(request,'ListarTelevisores.html',context)

def MostrarTelevisores(request):
    
    usuario_actual = request.user.username
    
    Query = Televisor.objects.filter(calificacion__correo__isnull=True ).order_by('modelo').values('calificacion__calificacionusuario','modelo','observaciones','marca','precio','tamanopantalla','resolucion','tipodisplay','urlwalmart','urlbb')| Televisor.objects.all().filter(calificacion__correo=usuario_actual ).order_by('modelo').values('calificacion__calificacionusuario','modelo','observaciones','marca','precio','tamanopantalla','resolucion','tipodisplay','urlwalmart','urlbb')
    print(Query.query)
    context = {
                    'ListaTelevisores':Query,                    
                    }
    
    return render(request,'MostrarTelevisores.html',context)

@csrf_exempt
def VerRecomendaciones(request):
    usuario_actual = request.user.username
    query = recomendacion(usuario_actual)
    dicc = {}
    contador = 0
    for i in query:
        if contador >9:
            break
        else:
            mod = Precision.objects.all().filter(modelo=i,usuario=usuario_actual).first()
            if(mod != None):
                mod = mod.calificacion
            dicc[i] = mod
            contador += 1
    context={
            'recomendaciones':dicc
            }
    return render(request,'VerRecomendaciones.html',context)

@csrf_exempt
def ModalTelevisores(request):
    
    if(request.method=="POST"):
        context = {
                'datos':{'observaciones':request.POST.get('observaciones'),'modelo':request.POST.get('modelo'),'calificacion':request.POST.get('calificacion'),'link1':request.POST.get('link1'),'link2':request.POST.get('link2')},
                }
        
    return render(request,'ModalTelevisores.html',context)

def PlotGraficos(columna,keys,valores):
    fig = plt.figure() # Figure   
    ax = fig.add_subplot(111) # Axes
    xx = range(len(valores))
    ax.bar(xx, valores, width=0.8, align='center')
    ax.set_xticks(xx)
    ax.set_xticklabels(keys, rotation='vertical')
    ax.set_title(columna.upper()+" Televisores")    
    ax.set_xlabel(columna)
    ax.set_ylabel('Cantidad')    
    ax.plot() 
    fig.tight_layout()
    figure = plt.gcf()
    buf = io.BytesIO()
    
    figure.savefig(buf, format='png', transparent=True, quality=100, dpi=200)    
    
    buf.seek(0)
    imsrc = base64.b64encode(buf.read())
    imuri = 'data:image/png;base64,{}'.format(urllib.parse.quote(imsrc))
    return imuri
    

@csrf_exempt
def EstadisticasTelevisores(request):
    resultado = []
    
    qs = Televisor.objects.all()
    df = read_frame(qs)    
    
    listaColumnas = ['marca','tamanopantalla','tipodisplay','resolucion']
    
    
    for columna in listaColumnas:
        Busqueda =  df.groupby([columna])[columna].count()
        EstadisticaDescriptiva = list(Busqueda.describe())
        keys = Busqueda.keys()
        valores =list(Busqueda)
        imuri = PlotGraficos(columna,keys,valores)    
    
        Estadistica = {
                          'count':EstadisticaDescriptiva[0],
                          'mean':EstadisticaDescriptiva[1],
                          'std':EstadisticaDescriptiva[2],
                          'min':EstadisticaDescriptiva[3],
                          'v25':EstadisticaDescriptiva[4],
                          'v50':EstadisticaDescriptiva[5],
                          'v75':EstadisticaDescriptiva[6],
                          'max':EstadisticaDescriptiva[7], 
                       }
        resultado.append(   {    
                           'name':columna,
                           'plot': imuri,
                           'estadistica':Estadistica,
                            })
                       
    context = {
                'resultado':resultado
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
            usuariob = User.objects.create_user(request.POST.get('email'),request.POST.get('email'),request.POST.get('password'),first_name=request.POST.get('nombre'))
            tabla_usuario = Usuario(correo = request.POST.get('email'),contrasena = request.POST.get('password'),nombre = request.POST.get('nombre'))
            usuariob.save()
            tabla_usuario.save()
            #context = {
            #        'mensaje':{'usuario':request.POST.get('email'),'mensaje':'Registrado Correctamente.'},                    
            #        }
            messages.success(request,'El usuario '+request.POST.get('email')+' se ha registrado correctamente')
    
            return render(request,'login.html')  
        
        except IntegrityError:
            #context = {
            #        'mensaje':{'usuario':request.POST.get('email'),'mensaje':'Error usuario ya registrado.'},                    
            #        }
            messages.error(request,'El usuario '+request.POST.get('email')+' ya esta registrado')
            return render(request,'registro.html')      
            
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
                
                return redirect('GestionTelevisores')
            
            else:
                return redirect('MostrarTelevisores')
        else:
            messages.error(request,'Error de inicio de sesión')
            return redirect('login')
    
    
    return render(request,'registro.html')



def VerPerfilUsuario(request):
    usuario_actual = request.user.username
    perfilusuario = perfil_usuario(usuario_actual )
    
    precision =MostrarPrecisionUsuario()
    perfilusuario['precision'] = precision
    context = {'datos':perfilusuario,'precision':precision}
    
    print(perfilusuario)
    return render(request,'VerPerfilUsuario.html',context)