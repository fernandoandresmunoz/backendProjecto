from rest_framework import serializers
from .models import Lienzo, Punto, Funcion, Integral, Derivada, Nodo, Matriz

# Serializador para el modelo Punto.
# Usaremos este serializador anidado dentro de Lienzo.
class PuntoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Punto
        fields = ['id', 'x', 'y', 'lienzo', 'color', 'etiqueta'] # Incluimos los campos relevantes

        # Excluimos 'lienzo' aquí porque se manejará en la vista y en el serializador padre (Lienzo)
        read_only_fields = ('id',)


# Serializador para el modelo Lienzo.
# Incluye una representación anidada de todos sus Puntos.
class LienzoSerializer(serializers.ModelSerializer):
    # La clave 'puntos' proviene de related_name='puntos' en el ForeignKey del modelo Punto.
    puntos = PuntoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lienzo
        # Incluye todos los campos de Lienzo, y automáticamente el campo 'id'
        fields = '__all__'
        read_only_fields = ('id', 'fecha_creacion', 'fecha_actualizacion')
        
# Por el momento, no incluimos Funcion, Integral ni Derivada.
# Solo nos enfocamos en validar Lienzo y Punto.

class PuntoSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Punto
        fields = ['id', 'x', 'y']
        read_only_fields = ['id', 'x', 'y']

from rest_framework import serializers
from .models import Recta # Asumiendo que has importado Recta

class RectaSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Recta.
    Incluye las propiedades matemáticas calculadas.
    """
    # Estos campos se calculan en el modelo, el cliente solo los puede leer.
    pendiente = serializers.ReadOnlyField()
    interseccion_y = serializers.ReadOnlyField()
    # Se sobrescriben p1 y p2 para usar el serializador anidado.
    # read_only=True es crucial para que la API siga esperando IDs en el POST.
    # p1 = PuntoSimpleSerializer(read_only=True)
    # p2 = PuntoSimpleSerializer(read_only=True)
    p1_data = serializers.SerializerMethodField()
    p2_data = serializers.SerializerMethodField()


    def get_p1_data(self, obj: Recta):
        # Utiliza el PuntoSimpleSerializer para serializar el objeto p1 relacionado
        return PuntoSimpleSerializer(obj.p1).data

    # Métodos para obtener los datos anidados de p2
    def get_p2_data(self, obj: Recta):
        # Utiliza el PuntoSimpleSerializer para serializar el objeto p2 relacionado
        return PuntoSimpleSerializer(obj.p2).data
    
    class Meta:
        model = Recta
        fields = [
            'id', 'lienzo', 'p1', 'p2', 'p1_data', 'p2_data', 'color', 'grosor_linea', 
            'pendiente', 'interseccion_y'
        ]
        read_only_fields = ('id', 'pendiente', 'interseccion_y')




from rest_framework import serializers
from .models import Nodo # Asegúrate de importar Nodo

# # Definición del Serializador del Nodo
# class NodoSerializer(serializers.ModelSerializer):
#     """
#     Serializador para el modelo Nodo (estructuras de árbol).
#     Maneja la relación recursiva 'padre'.
#     """
    
#     # Campo para la lectura: muestra los IDs de los nodos hijos de este nodo.
#     # No anidamos los objetos completos para prevenir ciclos infinitos.
#     hijos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
#     class Meta:
#         model = Nodo
#         fields = [
#             'id', 
#             'padre', # Para escritura: acepta el ID del nodo padre (o null)
#             'nombre',
#             'hijos' # Para lectura: lista de IDs de los hijos
#         ]
#         read_only_fields = ('id', 'hijos')



class NodoSerializer(serializers.ModelSerializer):
    # Campo para recibir el ID del padre del frontend, no es un campo del modelo.
    # Write_only=True asegura que solo se use para entrada de datos, no para la salida JSON.
    padreId = serializers.PrimaryKeyRelatedField(
        source='padre', # <--- ESTO ASOCIA 'padreId' entrante al campo 'padre' del modelo
        queryset=Nodo.objects.all(), 
        allow_null=True, # Permite que el nodo raíz no tenga padre
        required=False,
        write_only=True
    )

    class Meta:
        model = Nodo
        # Incluimos 'padre' para la salida (GET) y 'padreId' para la entrada (POST)
        fields = ['id', 'nombre', 'padre', 'padreId', 'matriz_ac', 'is_leaf'] 
        read_only_fields = ['id'] # El ID es de solo lectura


    def to_representation(self, instance):
        """
        Personaliza la representación del objeto para la salida (GET).
        Aseguramos que solo se muestre el ID del padre, no el objeto completo,
        y que se elimine el campo temporal 'padreId'.
        """
        # Obtenemos la representación base (incluye 'padre' como objeto o PK)
        representation = super().to_representation(instance)
        
        # Si el nodo tiene un padre, reemplazamos la representación por solo su ID
        if instance.padre:
            representation['padre'] = instance.padre.id
        else:
            representation['padre'] = None
            
        # Limpiamos el campo de entrada 'padreId' de la salida JSON
        if 'padreId' in representation:
            del representation['padreId']
            
        return representation



class MatrizSerializer(serializers.ModelSerializer):
    """
    Serializador que convierte el objeto Matriz del backend en JSON y viceversa.
    Incluye todos los campos para permitir el CRUD completo de la matriz.
    """
    class Meta:
        model = Matriz
        # Incluir todos los campos definidos en el modelo.
        fields = '__all__' 
