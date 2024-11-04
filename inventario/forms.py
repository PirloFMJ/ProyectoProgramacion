from django import forms
from .models import Producto, Cliente, CategoriaProducto, Empleado, Proveedor

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'descripcion_producto', 'precio_compra', 'precio_venta', 'id_categoria']
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_producto': forms.Textarea(attrs={'class': 'form-control'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control'}),
            'id_categoria': forms.Select(attrs={'class': 'form-control'}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nit_cliente', 'nombre_completo', 'num_telefono', 'email']
        widgets = {
            'nit_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'num_telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    # Validacion de nit
    def clean_nit_cliente(self):
        nit_cliente = self.cleaned_data.get('nit_cliente')
        if not nit_cliente:  # Valida que el campo no esté vacío
            raise forms.ValidationError("El NIT del cliente es obligatorio.")
        return nit_cliente


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = ['nombre_categoria', 'descripcion_categoria']
        widgets = {
            'nombre_categoria': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion_categoria': forms.Textarea(attrs={'class': 'form-control'}),
        }


class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre_usuario', 'puesto']  # Solo incluimos los campos necesarios para crear un empleado
        widgets = {
            'nombre_usuario': forms.TextInput(attrs={'class': 'form-control'}),
            'puesto': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nit_proveedor', 'nombre_proveedor', 'direccion_proveedor', 'telefono_proveedor']
        widgets = {
            'nit_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion_proveedor': forms.Textarea(attrs={'class': 'form-control'}),
            'telefono_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class LoginForm(forms.Form):
        username = forms.CharField(
            label="Usuario",
            widget=forms.TextInput(attrs={'class': 'form-control'})
        )
        password = forms.CharField(
            label="Contraseña",
            widget=forms.PasswordInput(attrs={'class': 'form-control'})
        )