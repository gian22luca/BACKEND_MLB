from rest_framework import serializers
from .models import Usuario, Producto, Pedido

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario 
        fields = ['id_usuario', 'nombre', 'apellido', 'email', 'empleado']
        read_only_fields = ['id_usuario']


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id_producto', 'nombre', 'descripcion', 'precio', 'stock', 'talle']
        
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