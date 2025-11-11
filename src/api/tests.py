from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from .models import Producto, CustomUser
from rest_framework import status


class ProductoAPITestCase(APITestCase):
   

    def setUp(self):
       
        
        self.client = APIClient()

       
        self.user = CustomUser.objects.create(
            email='test@test.com',
            password='password123.',
            first_name='Test',
            last_name='User'
        )

        
        self.productos_url = '/api/producto/'

        self.producto1 = Producto.objects.create(
            name='Tablero de Pulsadores',
            description='8 pulsadores con luces LED',
            cost =  100
            
            
        )

        self.producto2 = Producto.objects.create(
            name='Pantalla translucida Led',
            description='Pantallla translucidad publicidad 1000mm x 250mm',
            cost =  600
        )

    # GENERAR CASOS DE PRUEBA
    def test_obtener_lista_productos(self):
       

        
        response = self.client.get(self.productos_url)

       
        with self.subTest("Verificando código de estado"):
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        print("Lista de productos obtenida exitosamente - Código 200")

        
        with self.subTest("Verificando cantidad de productos"):
            self.assertGreaterEqual(len(response.data),4)
        print("Cantidad de productos es correcta")



    def test_obtener_producto_inexistente(self):
        
        url = f'{self.productos_url}9999/'
       
        self.client.force_authenticate(user=self.user)

       
        response = self.client.get(url)
        
        with self.subTest("Verificando codígo de estado 404"):
            self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print("Error 404 recibido")


        self.assertEqual(response.data['error'],'Producto no encontrado')
    




