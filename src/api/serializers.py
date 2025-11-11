from rest_framework import serializers
from .models import Usuario, Producto, Pedido
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

def validar_caracteres_alfebeticos(value):
            """Validador para solo alfanuméricos"""
            import re
            if not re.match(r'^[a-zA-Z0-9\s]+$', value):
                raise serializers.ValidationError(
                    'Solo se permiten letras, números y espacios.'
                    )
            return value



class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario 
        fields = ['id_usuario', 'nombre', 'apellido', 'email', 'empleado']
        read_only_fields = ['id_usuario']
        validators = [validar_caracteres_alfebeticos]
       


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id_producto', 'nombre', 'descripcion', 'precio', 'stock']
        validators = [validar_caracteres_alfebeticos]
        read_only_fields = ['id_producto']

    def validate_precio(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio no puede ser negativo.")
        return value
    
    

class PedidoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pedido 
        fields = ['id_pedido', 'usuario', 'producto', 'cantidad', 'fecha_pedido', 'estado', 'precio_total']
        read_only_fields = ['id_pedido', 'fecha_pedido']
    def validar_precio_total(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio total no puede ser negativo.")
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
       
        token['email'] = user.email
        token['phone'] = getattr(user, 'phone', None) 
        token['is_staff'] = user.is_staff
        return token      