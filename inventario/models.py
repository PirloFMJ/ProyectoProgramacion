from django.db import models

class CategoriaProducto(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField(max_length=100)
    descripcion_categoria = models.TextField()

    def __str__(self):
        return self.nombre_categoria

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_categoria = models.ForeignKey(CategoriaProducto, on_delete=models.CASCADE)
    nombre_producto = models.CharField(max_length=100)
    descripcion_producto = models.TextField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre_producto

class Empleado(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=100)
    puesto = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_usuario

class Cliente(models.Model):
    nit_cliente = models.CharField(max_length=20, primary_key=True)
    nombre_completo = models.CharField(max_length=100)
    num_telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nombre_completo

class Proveedor(models.Model):
    nit_proveedor = models.CharField(max_length=20, primary_key=True)
    nombre_proveedor = models.CharField(max_length=100)
    direccion_proveedor = models.TextField()
    telefono_proveedor = models.CharField(max_length=15)

    def __str__(self):
        return self.nombre_proveedor

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_disponible = models.IntegerField()
    fecha_expiracion = models.DateField()
    esta_vencido = models.BooleanField(default=False)

    def __str__(self):
        return f"Inventario de {self.id_producto}"

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    nit_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_venta = models.DateField(auto_now_add=True)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Venta {self.id_venta}"

    def calcular_total(self):
        self.total_venta = sum(
            detalle.total_producto for detalle in self.detalleventa_set.all()
        )

class DetalleVenta(models.Model):
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producto = models.IntegerField()
    total_producto = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"Detalle de venta {self.id_venta}"

    def calcular_total_producto(self):
        # Calcula el subtotal para el producto (precio_venta * cantidad)
        self.total_producto = self.id_producto.precio_venta * self.cantidad_producto

class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    nit_proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_compra = models.DateField(auto_now_add=True)
    total_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Compra {self.id_compra}"

    def calcular_total(self):
        self.total_compra = sum(
            detalle.total_producto for detalle in self.detallecompra_set.all()
        )

class DetalleCompra(models.Model):
    id_compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    id_producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_producto = models.IntegerField()
    total_producto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_expiracion = models.DateField(null=True, blank=True)  # Nuevo campo de fecha de caducidad

    def __str__(self):
        return f"Detalle de compra {self.id_compra}"

    def calcular_total_producto(self):
        # Calcula el subtotal para el producto (precio_compra * cantidad)
        self.total_producto = self.id_producto.precio_compra * self.cantidad_producto