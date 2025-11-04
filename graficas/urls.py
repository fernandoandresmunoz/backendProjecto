from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Crea un router para registrar automáticamente las rutas de los ViewSets
router = DefaultRouter()
router.register(r'lienzos', views.LienzoViewSet)
router.register(r'puntos', views.PuntoViewSet)
router.register(r'rectas', views.RectaViewSet)
router.register(r'nodos', views.NodoViewSet)
router.register(r'matrices', views.MatrizViewSet)

# Las URLs de la API ahora son determinadas automáticamente por el router.
urlpatterns = [
    # Esto incluirá /lienzos/ y /puntos/
    path('', include(router.urls)),
]
