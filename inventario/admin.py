from django.contrib import admin
from .models import (
    CategoriaProducto,
    Producto,
    Empleado,
    Cliente,
    Proveedor,
    Inventario,
    Venta,
    DetalleVenta,
    Compra,
    DetalleCompra
)

# Registrar los modelos en el admin
admin.site.register(CategoriaProducto)
admin.site.register(Producto)
admin.site.register(Empleado)
admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Inventario)
admin.site.register(Venta)
admin.site.register(DetalleVenta)
admin.site.register(Compra)
admin.site.register(DetalleCompra)