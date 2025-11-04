from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .serializers import LienzoSerializer, PuntoSerializer, RectaSerializer, MatrizSerializer
from .models import Lienzo, Punto, Recta, Matriz
from django_filters.rest_framework import DjangoFilterBackend 



# Vista para manejar las operaciones CRUD del Lienzo


class LienzoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite crear, ver, editar y eliminar Lienzos.
    """
    queryset = Lienzo.objects.all().order_by('-fecha_creacion')
    serializer_class = LienzoSerializer
    
    # Nota: Aquí podríamos añadir lógica de permisos o filtrado por usuario más adelante.

# Vista para manejar las operaciones CRUD del Punto
class PuntoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite crear, ver, editar y eliminar Puntos.
    """
    queryset = Punto.objects.all()
    serializer_class = PuntoSerializer

    filter_backends = [DjangoFilterBackend]

    filterset_fields = ['lienzo']



    def perform_create(self, serializer):
        """
        Sobreescribe el método de creación para asignar el 'lienzo' 
        al punto si se proporciona el ID del lienzo en los datos POST.
        
        Nota: En un API RESTful más estricto, preferiríamos anidar la creación
        o usar una URL específica como /lienzos/{id}/puntos/
        """
        # Aquí puedes añadir lógica si necesitas obtener el lienzo a partir de la URL o del request
        # Por ahora, simplemente guardamos el punto:
        serializer.save()




class RectaViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite crear, ver, editar, y eliminar Rectas.
    Permite filtrar por lienzo_id (e.g., /rectas/?lienzo=1).
    """
    queryset = Recta.objects.all()
    serializer_class = RectaSerializer
    
    # Configuración del filtro por parámetro de consulta
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['lienzo']


from .models import Nodo
from .serializers import NodoSerializer # Asegúrate de importar NodoSerializer

# class NodoViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint que permite crear, ver, editar, y eliminar Nodos de un árbol.
#     """
#     queryset = Nodo.objects.all()
#     serializer_class = NodoSerializer
#     filterset_fields= ['padre']


#     def get_queryset(self):
#         # 1. Obtener el parámetro de la URL
#         padre_id = self.request.query_params.get('padre_id')
#         all_nodes = self.request.query_params.get('all', 'false').lower()
        
#         # 2. Filtrado por 'all=true' (mostrar todos)
#         if all_nodes == 'true':
#             return Nodo.objects.all()

#         # 3. Filtrado por 'padre_id=X' (mostrar hijos)
#         if padre_id is not None:
#             # Asegúrate de que el padre_id no sea una cadena vacía o inválida
#             try:
#                 # Filtrar todos los nodos que tengan este ID como su padre
#                 return Nodo.objects.filter(padre=padre_id)
#             except ValueError:
#                 # Si padre_id no es un entero, devolver un queryset vacío o manejar el error
#                 return Nodo.objects.none()

#         # 4. Comportamiento por defecto (mostrar solo las raíces)
#         # Esto sucede si no se pasa ni 'all' ni 'padre_id'.
#         return Nodo.objects.filter(padre__isnull=True)



class NodoViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite crear, ver, editar, y eliminar Nodos de un árbol.
    """
    # 1. Usamos el queryset completo como base para que el detalle siempre encuentre los nodos.
    queryset = Nodo.objects.all() 
    serializer_class = NodoSerializer
    filterset_fields= ['padre']


    def get_queryset(self):
        # **NOTA:** self.action es 'retrieve' para el detalle y 'list' para la lista.

        # Si la acción es 'retrieve' (GET /nodos/ID/) o cualquier otra acción de detalle (PUT/DELETE /nodos/ID/),
        # devolvemos el queryset base completo para que DRF pueda encontrar el nodo.
        if self.action not in ['list']:
            return Nodo.objects.all()

        # --- Lógica de filtrado SOLO para la acción 'list' (GET /nodos/) ---

        padre_id = self.request.query_params.get('padre_id')
        all_nodes = self.request.query_params.get('all', 'false').lower()
        
        # Filtrado por 'all=true'
        if all_nodes == 'true':
            return Nodo.objects.all()

        # Filtrado por 'padre_id=X' (mostrar hijos)
        if padre_id is not None:
            try:
                # Filtrar todos los nodos que tengan este ID como su padre
                return Nodo.objects.filter(padre=padre_id)
            except ValueError:
                return Nodo.objects.none()

        # Comportamiento por defecto para LISTADO (si no se pasa ningún query param)
        # Devolver solo las raíces para la carga inicial del árbol
        return Nodo.objects.filter(padre__isnull=True)




class MatrizViewSet(viewsets.ModelViewSet):
    queryset = Matriz.objects.all()
    serializer_class = MatrizSerializer




