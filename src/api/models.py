from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class  Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=60)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=40)
    id_usuario = models.AutoField(primary_key=True, unique=True)
    empleado = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.id_usuario} {self.nombre} {self.apellido}"
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    id_producto = models.AutoField(primary_key=True, unique=True)
    #archivo = models.FileField(upload_to='archivos/', null=True, blank=True)
    
    
    

    def __str__(self):
        return f"{self.id_producto} {self.nombre} {self.precio} {self.stock}"
    
class Pedido(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='usuarios')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='productos')
    cantidad = models.PositiveIntegerField()
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    id_pedido = models.AutoField(primary_key=True, unique=True)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        default='Pendiente',
        choices=[
            ('Pendiente', 'Pendiente'),
            ('Enviado', 'Enviado'),
            ('Entregado', 'Entregado'),
            ('Cancelado', 'Cancelado')
        ]
    )

    def __str__(self):
        return f"{self.id_pedido} {self.usuario} {self.producto} {self.cantidad} {self.fecha_pedido} {self.estado}"

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    
