from django.db import models

# Create your models here.
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
    talle = models.CharField(
        max_length=5,
        default='M',
        choices=[
            ('XS', 'Extra Small'),
            ('S', 'Small'),
            ('M', 'Medium'),
            ('L', 'Large'),
            ('XL', 'Extra Large'),
            ('XXL', 'Double Extra Large')
        ]
    )
    

    def __str__(self):
        return f"{self.id_producto} {self.nombre} {self.precio} {self.stock} {self.talle}"
    
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

