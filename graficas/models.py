from django.db import models

# Create your models here.


class Lienzo(models.Model):
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, 
        help_text="Fecha y hora en que se creó este lienzo."
    )

    # 4. Propiedad para un nombre legible (opcional)
    nombre = models.CharField(
        max_length=100,
        default="Nuevo Lienzo",
        help_text="Nombre descriptivo para el lienzo."
    ) 

    ancho = models.IntegerField(default=500)
    alto = models.IntegerField(default=500)
    color_fondo = models.CharField(max_length=100)

    ancho_eje_x = models.FloatField(default=16)
    ancho_eje_y  = models.FloatField(default=16)
    zoom = models.FloatField(default=16)


class Funcion(models.Model):
    lienzo = models.ForeignKey(Lienzo, on_delete=models.CASCADE)
    color = models.CharField(max_length=200)


class Integral(models.Model):
    color = models.CharField(max_length=200)
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE)


class Derivada(models.Model):
    funcion = models.ForeignKey(
        Funcion, 
        on_delete=models.CASCADE, 
        related_name='derivadas',
        help_text="La Función a la que pertenece esta Derivada."
    )
    
    color = models.CharField(
        max_length=7, 
        default="#2ca02c", 
        help_text="Color de la línea de la derivada (código hex)."
    )
    grosor_linea = models.IntegerField(
        default=1,
        help_text="Grosor de la línea de la derivada en píxeles."
    )
    
    punto_x = models.FloatField(
        help_text="El valor x donde se traza la línea tangente/derivada."
    )
    
    def __str__(self):
        return f"Derivada de {self.funcion.expresion} en x={self.punto_x}"

class Punto(models.Model):
    lienzo = models.ForeignKey(
        Lienzo, 
        on_delete=models.CASCADE,
        related_name='puntos',
        help_text="El Lienzo al que pertenece este Punto."
    )
    x = models.FloatField(help_text="Coordenada X del punto.")
    y = models.FloatField(help_text="Coordenada Y del punto.")
    color = models.CharField(
        max_length=7, 
        default="#d62728", 
        help_text="Color del punto (código hex)."
    )
    etiqueta = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Etiqueta opcional para el punto (ej. 'Máximo', 'A')."
    )

    def __str__(self):
        return f"Punto ({self.x}, {self.y}) en {self.lienzo.nombre}"



class Recta(models.Model):
    # La asociación directa y necesaria al Lienzo
    lienzo = models.ForeignKey(
        'Lienzo', 
        on_delete=models.CASCADE,
        related_name='rectas',
        help_text="El Lienzo al que pertenece esta Recta."
    )


# Puntos que definen la recta
    p1 = models.ForeignKey(
        'Punto', 
        on_delete=models.CASCADE, 
        related_name='rectas_p1',
        help_text="Punto inicial (x1, y1) de la Recta."
    )
    p2 = models.ForeignKey(
        'Punto', 
        on_delete=models.CASCADE, 
        related_name='rectas_p2',
        help_text="Punto final (x2, y2) de la Recta."
    )

    # Propiedades de estilo
    color = models.CharField(
        max_length=7, 
        default="#1f77b4", 
        help_text="Color de la línea (código hex)."
    )
    grosor_linea = models.IntegerField(
        default=2,
        help_text="Grosor de la línea en píxeles."
    )






class Nodo(models.Model):
    """
    Representa un nodo en una estructura de árbol.
    La relación recursiva 'padre' permite construir la jerarquía.
    """
    
    # Campo para la relación recursiva: apunta al mismo modelo 'Nodo'.
    # null=True y blank=True son obligatorios para permitir que el nodo raíz no tenga padre.
    nombre = models.CharField(max_length=200)
    padre = models.ForeignKey(
        'self',  # Se referencia a sí mismo
        on_delete=models.SET_NULL,  # Si el padre se borra, el hijo queda sin padre (null)
        null=True,
        blank=True,
        related_name='hijos',  # Permite acceder a los hijos de un nodo: mi_nodo.hijos.all()
        help_text="Referencia al nodo padre. Es nulo para la raíz del árbol."
    )
    matriz_ac = models.OneToOneField(
        'Matriz',  # Referencia al modelo Matriz
        on_delete=models.SET_NULL,  # Si la Matriz se borra, el Nodo queda sin referencia (NULL)
        null=True,                  # Permite que la relación sea opcional (crucial)
        blank=True,                 # Permite que el campo esté vacío en formularios
        related_name='nodo_asociado', # Permite acceder al Nodo desde la Matriz (ej: mi_matriz.nodo_asociado)
        help_text="La Matriz de estado inicial del Autómata Celular (solo para nodos hoja)."
    )
    is_leaf = models.BooleanField(
        default=False, # Por defecto, asumimos que puede ser compuesto
        help_text="Indica si el nodo es una hoja (no tiene afluentes)."
    )


class Matriz(models.Model):
    """
    Modelo para almacenar la matriz de datos de un Autómata Celular. 
    Se utiliza el campo JSONField para la persistencia de la estructura 2D.
    """
    # Relación: Si borras el Lienzo, borra la matriz. (Manteniendo el comentario para referencia)
    # lienzo = models.ForeignKey(Lienzo, on_delete=models.CASCADE, related_name='matrices')
    
    nombre = models.CharField(max_length=255, default="Nueva Matriz")
    
    # 1. Almacenamiento de la Estructura 2D (Array de Arrays)
    # models.JSONField es la forma estándar en Django (3.1+) para almacenar estructuras JSON.
    datos_matriz = models.JSONField(default=list) 
    
    # 2. Metadatos del Autómata
    filas = models.IntegerField(default=10)
    columnas = models.IntegerField(default=10)
    generacion = models.IntegerField(default=0)
    estado_actual = models.CharField(max_length=50, default="Inicial") # Por ejemplo: 'PAUSADO', 'RUNNING'

    fecha_creacion = models.DateTimeField(auto_now_add=True)


    green_rule = models.CharField(max_length=200, default="")
    blue_rule = models.CharField(max_length=200, default="")
    gray_rule = models.CharField(max_length=200, default="")
    brown_rule = models.CharField(max_length=200, default="")
    red_rule = models.CharField(max_length=200, default="")

    # cada cuantos segundos tiene que avanzar una generacion ( milisegundos )
    velocidad = models.IntegerField(default=250)

    # cada cuantas generaciones se tiene que guardar el automata
    intervalo_almacenamiento = models.IntegerField(default=20)
    
    class Meta:
        verbose_name_plural = "Matrices"
        
    def __str__(self):
        return f"Matriz {self.nombre} ({self.filas}x{self.columnas}) - Estado: {self.estado_actual}"