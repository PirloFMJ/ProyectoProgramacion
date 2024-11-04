from django.urls import path
from .views import listar_ventas, detalle_venta
from .views import (
    crear_producto, crear_cliente, listar_clientes, crear_categoria, listar_categorias, crear_empleado, listar_empleados,
    crear_proveedor, listar_proveedores, listar_productos, inicio_view, venta_view, compra_view, completar_compra, completar_venta,
    inventario_view, login_view
)

urlpatterns = [
    path('login/', login_view, name='login'),  # Ruta de login
    path('inicio/', inicio_view, name='inicio'),  # Ruta de inicio que verifica el grupo del usuario
    path('producto/crear/', crear_producto, name='crear_producto'),
    path('productos/', listar_productos, name='productos_listar'),
    path('cliente/crear/', crear_cliente, name='crear_cliente'),
    path('clientes/', listar_clientes, name='clientes_listar'),
    path('categoria/crear/', crear_categoria, name='crear_categoria'),
    path('categorias/', listar_categorias, name='categorias_listar'),
    path('empleado/crear/', crear_empleado, name='crear_empleado'),
    path('empleados/', listar_empleados, name='empleados_listar'),
    path('proveedor/crear/', crear_proveedor, name='crear_proveedor'),
    path('proveedores/', listar_proveedores, name='proveedores_listar'),
    path('venta/', venta_view, name='venta'),
    path('compra/', compra_view, name='compra'),
    path('completar_compra/', completar_compra, name='completar_compra'),
    path('completar_venta/', completar_venta, name='completar_venta'),
    path('inventario/', inventario_view, name='inventario'),
    path('ventas/', listar_ventas, name='ventas_listar'),
    path('ventas/<int:venta_id>/', detalle_venta, name='detalle_venta'),
    # Redirige la raíz al login
    path('', login_view),
]