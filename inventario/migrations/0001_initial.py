# Generated by Django 5.1.2 on 2024-11-03 01:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriaProducto',
            fields=[
                ('id_categoria', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_categoria', models.CharField(max_length=100)),
                ('descripcion_categoria', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('nit_cliente', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre_completo', models.CharField(max_length=100)),
                ('num_telefono', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_usuario', models.CharField(max_length=100)),
                ('puesto', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('nit_proveedor', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre_proveedor', models.CharField(max_length=100)),
                ('direccion_proveedor', models.TextField()),
                ('telefono_proveedor', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Compra',
            fields=[
                ('id_compra', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_compra', models.DateField(auto_now_add=True)),
                ('total_compra', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.empleado')),
                ('nit_proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id_producto', models.AutoField(primary_key=True, serialize=False)),
                ('nombre_producto', models.CharField(max_length=100)),
                ('descripcion_producto', models.TextField()),
                ('precio_compra', models.DecimalField(decimal_places=2, max_digits=10)),
                ('precio_venta', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.categoriaproducto')),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id_inventario', models.AutoField(primary_key=True, serialize=False)),
                ('cantidad_disponible', models.IntegerField()),
                ('fecha_expiracion', models.DateField()),
                ('esta_vencido', models.BooleanField(default=False)),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.producto')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_producto', models.IntegerField()),
                ('total_producto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_compra', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.compra')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.producto')),
            ],
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id_venta', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_venta', models.DateField(auto_now_add=True)),
                ('total_venta', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.empleado')),
                ('nit_cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad_producto', models.IntegerField()),
                ('total_producto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.producto')),
                ('id_venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.venta')),
            ],
        ),
    ]
