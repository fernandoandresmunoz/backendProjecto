from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .models import Lienzo, Punto, Recta, Nodo, Matriz


class LienzoViewSetTests(APITestCase):
    """
    Tests basicos del endpoint /graficas/lienzos/
    """

    def setUp(self):
        self.client = APIClient()
        self.lienzo = Lienzo.objects.create(
            nombre='Lienzo de prueba',
            ancho=500,
            alto=500,
            color_fondo='#ffffff',
        )

    def test_listar_lienzos(self):
        response = self.client.get('/graficas/lienzos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_lienzo(self):
        data = {
            'nombre': 'Nuevo lienzo',
            'ancho': 800,
            'alto': 600,
            'color_fondo': '#000000',
        }
        response = self.client.post('/graficas/lienzos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lienzo.objects.count(), 2)

    def test_obtener_detalle_lienzo(self):
        response = self.client.get('/graficas/lienzos/%d/' % self.lienzo.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Lienzo de prueba')

    def test_obtener_lienzo_inexistente(self):
        response = self.client.get('/graficas/lienzos/99999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_actualizar_lienzo(self):
        response = self.client.patch(
            '/graficas/lienzos/%d/' % self.lienzo.id,
            {'nombre': 'Lienzo editado'},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lienzo.refresh_from_db()
        self.assertEqual(self.lienzo.nombre, 'Lienzo editado')

    def test_eliminar_lienzo(self):
        response = self.client.delete('/graficas/lienzos/%d/' % self.lienzo.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lienzo.objects.count(), 0)


class PuntoViewSetTests(APITestCase):
    """
    Tests basicos del endpoint /graficas/puntos/
    """

    def setUp(self):
        self.client = APIClient()
        self.lienzo = Lienzo.objects.create(nombre='Lienzo puntos', color_fondo='#ffffff')
        self.punto = Punto.objects.create(lienzo=self.lienzo, x=1.0, y=2.0)

    def test_listar_puntos(self):
        response = self.client.get('/graficas/puntos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_punto(self):
        data = {
            'lienzo': self.lienzo.id,
            'x': 5,
            'y': 10,
            'etiqueta': 'A',
        }
        response = self.client.post('/graficas/puntos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Punto.objects.count(), 2)

    def test_filtrar_puntos_por_lienzo(self):
        response = self.client.get('/graficas/puntos/?lienzo=%d' % self.lienzo.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_str_punto(self):
        self.assertIn('Punto', str(self.punto))


class RectaViewSetTests(APITestCase):
    """
    Tests basicos del endpoint /graficas/rectas/
    """

    def setUp(self):
        self.client = APIClient()
        self.lienzo = Lienzo.objects.create(nombre='Lienzo rectas', color_fondo='#ffffff')
        self.p1 = Punto.objects.create(lienzo=self.lienzo, x=0, y=0)
        self.p2 = Punto.objects.create(lienzo=self.lienzo, x=5, y=5)
        self.recta = Recta.objects.create(lienzo=self.lienzo, p1=self.p1, p2=self.p2)

    def test_listar_rectas(self):
        response = self.client.get('/graficas/rectas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_recta(self):
        data = {
            'lienzo': self.lienzo.id,
            'p1': self.p1.id,
            'p2': self.p2.id,
        }
        response = self.client.post('/graficas/rectas/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Recta.objects.count(), 2)

    def test_filtrar_rectas_por_lienzo(self):
        response = self.client.get('/graficas/rectas/?lienzo=%d' % self.lienzo.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class NodoViewSetTests(APITestCase):
    """
    Tests basicos del endpoint /graficas/nodos/
    """

    def setUp(self):
        self.client = APIClient()
        self.raiz = Nodo.objects.create(nombre='raiz')
        self.hijo = Nodo.objects.create(nombre='hijo', padre=self.raiz)

    def test_listar_nodos_por_defecto_solo_raices(self):
        response = self.client.get('/graficas/nodos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_listar_todos_los_nodos(self):
        response = self.client.get('/graficas/nodos/?all=true')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_listar_hijos_de_un_nodo(self):
        response = self.client.get('/graficas/nodos/?padre_id=%d' % self.raiz.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_crear_nodo(self):
        data = {'nombre': 'nuevo nodo'}
        response = self.client.post('/graficas/nodos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Nodo.objects.count(), 3)

    def test_obtener_detalle_nodo(self):
        response = self.client.get('/graficas/nodos/%d/' % self.hijo.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['padre'], self.raiz.id)

    def test_eliminar_nodo(self):
        response = self.client.delete('/graficas/nodos/%d/' % self.hijo.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Nodo.objects.count(), 1)


class MatrizViewSetTests(APITestCase):
    """
    Tests basicos del endpoint /graficas/matrices/
    """

    def setUp(self):
        self.client = APIClient()
        self.matriz = Matriz.objects.create(nombre='Matriz de prueba', filas=5, columnas=5)

    def test_listar_matrices(self):
        response = self.client.get('/graficas/matrices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_matriz(self):
        data = {
            'nombre': 'Nueva matriz',
            'filas': 10,
            'columnas': 10,
            'datos_matriz': [],
        }
        response = self.client.post('/graficas/matrices/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Matriz.objects.count(), 2)

    def test_obtener_detalle_matriz(self):
        response = self.client.get('/graficas/matrices/%d/' % self.matriz.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], 'Matriz de prueba')

    def test_actualizar_matriz(self):
        response = self.client.patch(
            '/graficas/matrices/%d/' % self.matriz.id,
            {'estado_actual': 'RUNNING'},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.matriz.refresh_from_db()
        self.assertEqual(self.matriz.estado_actual, 'RUNNING')

    def test_str_matriz(self):
        self.assertIn('Matriz de prueba', str(self.matriz))

    def test_paginacion_matrices(self):
        for i in range(15):
            Matriz.objects.create(nombre='Matriz %d' % i)
        response = self.client.get('/graficas/matrices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)


class RutasGeneralesTests(APITestCase):
    """
    Test de humo simple para asegurar que el pipeline detecte al menos un test.
    """

    def test_ejemplo(self):
        self.assertEqual(1, 1)
