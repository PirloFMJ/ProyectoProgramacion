from django.urls import path
from .views import login_view, inicio_view, cerrar_sesion
from .views import (crear_producto, crear_cliente, listar_clientes, crear_categoria, listar_categorias, crear_empleado, listar_empleados,
crear_proveedor, listar_proveedores, listar_productos, inicio, venta_view, compra_view, completar_compra, completar_venta, inventario_view,
editar_proveedor, eliminar_proveedor, editar_categoria, eliminar_categoria, editar_cliente, eliminar_cliente,
listar_compras, detalle_compra, editar_empleado, eliminar_empleado, editar_producto, eliminar_producto, listar_ventas, detalle_venta, reporte_ventas)
urlpatterns = [
path('producto/crear/', crear_producto, name='crear_producto'),
    path('productos/', listar_productos, name='productos_listar'),
    path('productos/editar/<int:producto_id>/', editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    path('cliente/crear/', crear_cliente, name='crear_cliente'),
    path('clientes/', listar_clientes, name='clientes_listar'),
    path('clientes/editar/<str:cliente_id>/', editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<str:cliente_id>/', eliminar_cliente, name='eliminar_cliente'),
    path('categoria/crear/', crear_categoria, name='crear_categoria'),
    path('categorias/', listar_categorias, name='categorias_listar'),
    path('categorias/editar/<int:categoria_id>/', editar_categoria, name='editar_categoria'),
    path('categorias/eliminar/<int:categoria_id>/', eliminar_categoria, name='eliminar_categoria'),
    path('empleado/crear/', crear_empleado, name='crear_empleado'),  # Ruta para crear empleado
    path('empleados/', listar_empleados, name='empleados_listar'),
    path('empleados/editar/<int:empleado_id>/', editar_empleado, name='editar_empleado'),
    path('empleados/eliminar/<int:empleado_id>/', eliminar_empleado, name='eliminar_empleado'),
    path('proveedor/crear/', crear_proveedor, name='crear_proveedor'),  # Ruta para crear proveedor
    path('proveedores/', listar_proveedores, name='proveedores_listar'),
    path('proveedores/editar/<str:proveedor_id>/', editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<str:proveedor_id>/', eliminar_proveedor, name='eliminar_proveedor'),
    path('venta/', venta_view, name='venta'),
    path('compra/', compra_view, name='compra'),
    path('compras/', listar_compras, name='compras_listar'),
    path('compras/<int:compra_id>/', detalle_compra, name='detalle_compra'),
    path('completar_compra/', completar_compra, name='completar_compra'),
    path('completar_venta/', completar_venta, name='completar_venta'),
    path('inventario/', inventario_view, name='inventario'),
    path('ventas/', listar_ventas, name='ventas_listar'),
    path('ventas/<int:venta_id>/', detalle_venta, name='detalle_venta'),
    path('login/', login_view, name='login'),  # Ruta de login
    path('inicio/', inicio_view, name='inicio'),  # Ruta de inicio que verifica el grupo del usuario
    path('reporte_ventas/', reporte_ventas, name='reporte_ventas'),
    # Redirige la raíz al login
    path('', login_view),
    path('logout/', cerrar_sesion, name='cerrar_sesion'),
]