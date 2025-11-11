from django.shortcuts import render
from django.http import HttpResponse , JsonResponse
from rest_framework.views import APIView
from .models import Usuario, Producto, Pedido, CustomUser
from .serializers import UsuarioSerializer, ProductoSerializer, PedidoSerializer
from rest_framework.response import Response
from django.db.models.deletion import RestrictedError
from rest_framework import status
from django.db.models import Q
#Permisos
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from utils.permission import TienePermisoModelo
#Paginación
from rest_framework.pagination import PageNumberPagination
from utils.pagination import CustomPagination
#Documentacion
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Response as OpenAPIResponse

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, ProductoSerializer
from rest_framework.viewsets import ModelViewSet
import logging

logger = logging.getLogger('api_vixel')

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




# Create your views here.
def inicio(request):
    mensaje = "<h1>¡Bienvenido a Vixel!</h1>"
    return HttpResponse(mensaje)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_info(request):
    """
        Información general de la API de Vixel.
    """
    response = {
        "message":"Bienvenido a la API de  Vixel",
        "version": "1.0"
    }
    return JsonResponse(response)


@api_view(['GET'])
def search_users_safe(request):
    query = request.GET.get('query','')

    users = CustomUser.objects.filter(
        Q(email__icontains=query) | Q(first_name__icontains=query)
    ).values('id','email')

    return Response({
        'count': users.count(),
        'result': list(users)
    })

class UsuarioAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser] 
    @swagger_auto_schema(
        operation_description="Obtener una lista de usuarios",
        responses={
            200: UsuarioSerializer(many=True),
            201: UsuarioSerializer,
            400: OpenAPIResponse(
                description="Error de validación",
                schema=UsuarioSerializer(many=True)
            ) 
        }
    )
    def get(self, request):
        usuario = Usuario.objects.all()
        paginator =CustomPagination()
        paginated_queryset = paginator.paginate_queryset(usuario, request)
        usuario_serializer = UsuarioSerializer(usuario, many=True)
        return paginator.get_paginated_response(usuario_serializer.data)
    
    @swagger_auto_schema(
        operation_description="Crear un nuevo usuario",
        request_body=UsuarioSerializer,
        responses={
            201: UsuarioSerializer,
            400: "Error de validación"
        }
    )
    def post(self, request):
        usuario_serializer = UsuarioSerializer(data=request.data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return Response(usuario_serializer.data, status=201)
        return Response(usuario_serializer.errors, status=400)

class UsuarioDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Obtener un usuario por ID",
        responses={
            200: UsuarioSerializer,
            404: "Usuario no encontrado"
        }
    )
    def get(self, request, pk):
        try:
            usuario = Usuario.objects.get(pk=pk)
            usuario_serializer = UsuarioSerializer(usuario)
            return Response(usuario_serializer.data)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
        operation_description="Actualizar un usuario por ID",
        request_body=UsuarioSerializer,
        responses={
            200: UsuarioSerializer,
            400: "Error de validación",
            404: "Usuario no encontrado"
        }
    )
    def put(self, request, pk):
        try:
            usuario = Usuario.objects.get(pk=pk)
            usuario_serializer = UsuarioSerializer(usuario, data=request.data)
            if usuario_serializer.is_valid():
                usuario_serializer.save()
                respuesta = {
                    "message": "Usuario actualizado correctamente",
                    "usuario": usuario_serializer.data
                }
                return Response(usuario_serializer.data)
            return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_description="Eliminar un usuario por ID",
        responses={
            204: "Usuario eliminado correctamente",
            404: "Usuario no encontrado",
            400: "No se puede eliminar el usuario porque tiene pedidos asociados"
        }
    )
    def delete(self, request, pk):
        try:
            usuario = Usuario.objects.get(pk=pk)
            usuario.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status.HTTP_404_NOT_FOUND)
        except RestrictedError:
            return Response({"error": "No se puede eliminar el usuario porque tiene pedidos asociados"}, status=status.HTTP_400_BAD_REQUEST)

class ProductoAPIView(APIView):
    permission_classes = [IsAuthenticated,TienePermisoModelo]
    @swagger_auto_schema(
        operation_description="Obtener una lista de productos",
        responses={
            200: ProductoSerializer(many=True),
            201: ProductoSerializer,
            400: "Error de validación"
        }
    )
    def get(self, request):
        logger.info("Obteniendo la lista de productos")
        producto = Producto.objects.all()
        paginator =CustomPagination()
        paginated_queryset = paginator.paginate_queryset(producto, request)
        producto_serializer = ProductoSerializer(producto, many=True)
        return paginator.get_paginated_response(producto_serializer.data) 
    @swagger_auto_schema(
        operation_description="Crear un producto",
        request_body=ProductoSerializer,
        responses={
            201: ProductoSerializer,
            400: "Error de validación"  
        }
    )
    def post(self, request):
        producto_serializer = ProductoSerializer(data=request.data)
        if producto_serializer.is_valid():
            producto_serializer.save()
            return Response(producto_serializer.data, status=status.HTTP_201_CREATED)
        return Response(producto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductoDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Obtener un producto por id",
        responses={
            200: ProductoSerializer,
            404: "Producto no encontrado"
        }
    )
    def get(self, request, pk):
        try:
            producto = Producto.objects.get(pk=pk)
            producto_serializer = ProductoSerializer(producto)
            return Response(producto_serializer.data)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
        operation_description="Actualizar un producto por ID",
        request_body=ProductoSerializer,
        responses={
            200: ProductoSerializer,
            400: "Error de validación",
            404: "Producto no encontrado"
        }
    )
    def put(self, request, pk):
        try:
            producto = Producto.objects.get(pk=pk)
            producto_serializer = ProductoSerializer(producto, data=request.data)
            if producto_serializer.is_valid():
                producto_serializer.save()
                respuesta = {
                    "message": "Producto actualizado correctamente",
                    "usuario": producto_serializer.data
                }
                return Response(respuesta,producto_serializer.data)
            return Response(producto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_description="Eliminar un producto por ID",
        responses={
            204: "Producto eliminado correctamente",
            404: "Producto no encontrado",
            400: "No se puede eliminar el producto porque tiene pedidos asociados"
        }
    )
    def delete(self, request, pk):
        try:
            producto = Producto.objects.get(pk=pk)
            producto.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Producto.DoesNotExist:
            return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except RestrictedError:
            return Response({"error": "No se puede eliminar el producto porque tiene pedidos asociados"}, status=status.HTTP_400_BAD_REQUEST)
    
class PedidoAPIView(APIView):
    permission_classes = [IsAuthenticated, TienePermisoModelo]
    @swagger_auto_schema(
        operation_description="Obtener una lista de pedidos",
        responses={
            200: PedidoSerializer(many=True),
            201: PedidoSerializer,
            400: "Error de validación"
        }
    )
    def get(self, request):
        pedido = Pedido.objects.all()
        pedido_serializer = PedidoSerializer(pedido, many=True)
        return Response(pedido_serializer.data)
    @swagger_auto_schema(
        operation_description="Crear un nuevo pedido",
        request_body=PedidoSerializer,
        responses={
            201: PedidoSerializer,
            400: "Error de validación"
        }
    )
    def post(self, request):
        pedido_serializer = PedidoSerializer(data=request.data)
        if pedido_serializer.is_valid():
            pedido_serializer.save()
            return Response(pedido_serializer.data, status=201)
        return Response(pedido_serializer.errors, status=400)
    
class PedidoDetalleAPIView(APIView):
    permission_classes = [IsAuthenticated,TienePermisoModelo]
    @swagger_auto_schema(
        operation_description="Obtener un pedido por ID",
        responses={
            200: PedidoSerializer,
            404: "Pedido no encontrado"
        }
    )
    def get(self, request, pk):
        try:
            pedido = Pedido.objects.get(pk=pk)
            pedido_serializer = PedidoSerializer(pedido)
            return Response(pedido_serializer.data)
        except Pedido.DoesNotExist:
            return Response({"error": "Pedido no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        operation_description="Actualizar un pedido por ID",
        request_body=PedidoSerializer,
        responses={
            200: PedidoSerializer,
            400: "Error de validación",
            404: "Pedido no encontrado"
        }
    )
    def put(self, request, pk):
        try:
            pedido = Pedido.objects.get(pk=pk)
            pedido_serializer = PedidoSerializer(pedido, data=request.data)
            if pedido_serializer.is_valid():
                pedido_serializer.save()
                respuesta = {
                    "message": "Pedido actualizado correctamente",
                    "usuario": pedido_serializer.data
                }
                return Response(respuesta,pedido_serializer.data)
            return Response(pedido_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Pedido.DoesNotExist:
            return Response({"error": "Pedido no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
        operation_description="Eliminar un pedido por ID",
        responses={
            204: "Pedido eliminado correctamente",
            404: "Pedido no encontrado",
            400: "No se puede eliminar el pedido porque tiene productos asociados"
        }   
    )
    def delete(self, request, pk):
        try:
            pedido = Pedido.objects.get(pk=pk)
            pedido.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Pedido.DoesNotExist:
            return Response({"error": "Pedido no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        

class ProductoViewSet(ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated, TienePermisoModelo]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated, TienePermisoModelo]
        return super().get_permissions()
    
    def get_queryset(self):
        stock = self.request.query_params.get('stock', None)
        if stock is not None:
            return Producto.objects.filter(stock__gt=0)
        return super().get_queryset()