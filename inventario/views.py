from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForm
from .forms import ProductoForm, ClienteForm, Cliente, CategoriaForm, CategoriaProducto, EmpleadoForm, ProveedorForm
from .models import Empleado, Proveedor, Producto, Venta, DetalleVenta
from .models import Compra, DetalleCompra, Inventario, Cliente
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import render, get_object_or_404
from .models import Venta, DetalleVenta


def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productos_listar')  # Redirigir a la lista de productos (cambia esto según tu URL)
    else:
        form = ProductoForm()
    return render(request, 'inventario/crear_producto.html', {'form': form})

def listar_productos(request):
    productos = Producto.objects.all()  # Obtiene todos los productos
    return render(request, 'inventario/listar_productos.html', {'productos': productos})

def crear_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes_listar')  # Redirigir a la lista de clientes (cambia esto según tu URL)
    else:
        form = ClienteForm()
    return render(request, 'inventario/crear_cliente.html', {'form': form})

def listar_clientes(request): #Sirve para ver la lista de clientes uqe hay
    clientes = Cliente.objects.all()  # Obtiene todos los clientes de la base de datos
    return render(request, 'inventario/listar_clientes.html', {'clientes': clientes})  # Renderiza el template con los clientes

def crear_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda la nueva categoría en la base de datos
            return redirect('categorias_listar')  # Redirige a la lista de categorías
    else:
        form = CategoriaForm()
    return render(request, 'inventario/crear_categoria.html', {'form': form})


from .models import CategoriaProducto

def listar_categorias(request):
    categorias = CategoriaProducto.objects.all()
    return render(request, 'inventario/listar_categorias.html', {'categorias': categorias})

def crear_empleado(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo empleado en la base de datos
            return redirect('empleados_listar')  # Redirige a la lista de empleados después de guardar
    else:
        form = EmpleadoForm()
    return render(request, 'inventario/crear_empleado.html', {'form': form})

def listar_empleados(request):
    empleados = Empleado.objects.all()  # Obtiene todos los empleados
    return render(request, 'inventario/listar_empleados.html', {'empleados': empleados})

def crear_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo proveedor en la base de datos
            return redirect('proveedores_listar')  # Redirige a la lista de proveedores después de guardar
    else:
        form = ProveedorForm()
    return render(request, 'inventario/crear_proveedor.html', {'form': form})

def listar_proveedores(request):
    proveedores = Proveedor.objects.all()  # Obtiene todos los proveedores
    return render(request, 'inventario/listar_proveedores.html', {'proveedores': proveedores})

def inicio(request):
    return render(request, 'inventario/inicio.html')


def venta_view(request):
    productos = Producto.objects.all()
    clientes = Cliente.objects.all()
    empleados = Empleado.objects.all()  # Obtener todos los empleados

    return render(request, 'inventario/venta.html', {
        'productos': productos,
        'clientes': clientes,
        'empleados': empleados  # Asegúrate de incluir empleados en el contexto
    })


def compra_view(request):
    productos = Producto.objects.all() # Obtiene todos los productos
    proveedores = Proveedor.objects.all() # Obtiene todos los proveedores
    empleados = Empleado.objects.all()  # Obtiene todos los empleados

    return render(request, 'inventario/compra.html', {
        'productos': productos,
        'proveedores': proveedores,
        'empleados': empleados
    })


@csrf_exempt  # Para depuración; en producción maneja CSRF adecuadamente
@transaction.atomic
def completar_compra(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            proveedor_id = data.get('proveedor')
            empleado_id = data.get('empleado')  # Obtener el empleado desde los datos JSON
            productos_compra = data.get('productos', [])
            total_compra = data.get('total')

            # Validar el proveedor
            try:
                proveedor = Proveedor.objects.get(nit_proveedor=proveedor_id)
            except Proveedor.DoesNotExist:
                return JsonResponse({'error': 'Proveedor no válido'}, status=400)

            # Validar el empleado
            try:
                empleado = Empleado.objects.get(id_usuario=empleado_id)
            except Empleado.DoesNotExist:
                return JsonResponse({'error': 'Empleado no válido'}, status=400)

            # Crear la compra con el proveedor y el empleado
            compra = Compra.objects.create(
                nit_proveedor=proveedor,
                id_usuario=empleado,  # Ahora asignamos un Empleado en lugar de request.user
                fecha_compra=timezone.now(),
                total_compra=total_compra
            )

            # Procesar los productos y actualizar el inventario
            for producto_data in productos_compra:
                producto_nombre = producto_data['nombre']
                fecha_expiracion = producto_data['fecha_expiracion']
                cantidad = int(producto_data['cantidad'])
                precio = float(producto_data['precio'])

                try:
                    producto = Producto.objects.get(nombre_producto=producto_nombre)
                except Producto.DoesNotExist:
                    return JsonResponse({'error': f'Producto con nombre {producto_nombre} no existe'}, status=400)

                DetalleCompra.objects.create(
                    id_compra=compra,
                    id_producto=producto,
                    cantidad_producto=cantidad,
                    total_producto=precio * cantidad
                )

                inventario_item, created = Inventario.objects.get_or_create(
                    id_producto=producto,
                    fecha_expiracion=fecha_expiracion,
                    defaults={'cantidad_disponible': 0}
                )

                if created:
                    inventario_item.cantidad_disponible = cantidad
                else:
                    inventario_item.cantidad_disponible += cantidad

                inventario_item.save()

            return JsonResponse({'success': 'Compra completada y inventario actualizado'})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


@csrf_exempt  # Solo para depuración; en producción maneja CSRF adecuadamente
@transaction.atomic
def completar_venta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            cliente_id = data.get('cliente')
            empleado_id = data.get('empleado')  # Obtener el empleado que realiza la venta
            productos_venta = data.get('productos', [])
            total_venta = data.get('total')

            # Validar el cliente
            try:
                cliente = Cliente.objects.get(nit_cliente=cliente_id)
            except Cliente.DoesNotExist:
                return JsonResponse({'error': 'Cliente no válido'}, status=400)

            # Validar el empleado
            try:
                empleado = Empleado.objects.get(id_usuario=empleado_id)
            except Empleado.DoesNotExist:
                return JsonResponse({'error': 'Empleado no válido'}, status=400)

            # Crear la venta
            venta = Venta.objects.create(
                nit_cliente=cliente,
                id_usuario=empleado,
                fecha_venta=timezone.now(),
                total_venta=total_venta
            )

            # Procesar cada producto en la venta
            for producto_data in productos_venta:
                producto_nombre = producto_data['nombre']
                cantidad_vendida = int(producto_data['cantidad'])
                precio = float(producto_data['precio'])

                # Obtener el producto por nombre
                try:
                    producto = Producto.objects.get(nombre_producto=producto_nombre)
                except Producto.DoesNotExist:
                    return JsonResponse({'error': f'Producto con nombre {producto_nombre} no existe'}, status=400)

                # Crear el detalle de la venta
                DetalleVenta.objects.create(
                    id_venta=venta,
                    id_producto=producto,
                    cantidad_producto=cantidad_vendida,
                    total_producto=precio * cantidad_vendida
                )

                # Actualizar el inventario, empezando por el producto más próximo a vencer
                inventarios = Inventario.objects.filter(id_producto=producto, cantidad_disponible__gt=0).order_by(
                    'fecha_expiracion')

                for inventario_item in inventarios:
                    if cantidad_vendida <= 0:
                        break  # Ya se ha cubierto toda la cantidad vendida

                    if inventario_item.cantidad_disponible >= cantidad_vendida:
                        # Si el inventario actual tiene suficiente cantidad para cubrir la venta
                        inventario_item.cantidad_disponible -= cantidad_vendida
                        inventario_item.save()
                        cantidad_vendida = 0
                    else:
                        # Si el inventario actual no es suficiente, reducir lo que se pueda y continuar con el siguiente
                        cantidad_vendida -= inventario_item.cantidad_disponible
                        inventario_item.cantidad_disponible = 0
                        inventario_item.save()

            # Si todo sale bien, devuelve un mensaje de éxito
            return JsonResponse({'success': 'Venta completada y inventario actualizado'})

        except Exception as e:
            # Capturar cualquier error inesperado y devolverlo en formato JSON
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)


def inventario_view(request):
    # Recuperar todos los productos del inventario
    inventario = Inventario.objects.all().order_by('id_producto', 'fecha_expiracion')
    return render(request, 'inventario/inventario.html', {'inventario': inventario})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('inicio')  # Redirige a la página de inicio si el login es exitoso
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginForm()

    return render(request, 'inventario/login.html', {'form': form})

@login_required
def inicio_view(request):
    user = request.user

    # Verifica si el usuario pertenece al grupo "Empleados"
    es_empleado = user.groups.filter(name="Empleados").exists()

    return render(request, 'inventario/inicio.html', {'es_empleado': es_empleado})

@login_required
def listar_ventas(request):
    ventas = Venta.objects.all()  # Obtiene todas las ventas
    return render(request, 'inventario/listar_ventas.html', {'ventas': ventas})

@login_required
def detalle_venta(request, venta_id):
    venta = get_object_or_404(Venta, id_venta=venta_id)  # Obtiene la venta específica por su ID
    detalles = DetalleVenta.objects.filter(id_venta=venta)  # Obtiene todos los productos en esa venta

    return render(request, 'inventario/detalle_venta.html', {
        'venta': venta,
        'detalles': detalles
    })
