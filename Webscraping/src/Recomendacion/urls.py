from django.urls import path
from Recomendacion.views import *
from rest_framework.routers import DefaultRouter

#router = DefaultRouter()
#router.register('sucursal', SucursalViewSet)

urlpatterns = [
                path('', index, name='index'),
                
                
                
              ]