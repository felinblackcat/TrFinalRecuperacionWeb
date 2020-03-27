from django.urls import path
from Recomendacion.views import index,runspider
from rest_framework.routers import DefaultRouter

#router = DefaultRouter()
#router.register('sucursal', SucursalViewSet)

urlpatterns = [
                path('', index, name='index'),
                path('runspider/', runspider, name='runspider'),
                
                
                
              ]