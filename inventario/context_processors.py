def grupo_empleado(request):
    if request.user.is_authenticated:
        es_empleado = request.user.groups.filter(name="Empleados").exists()
        return {'es_empleado': es_empleado}
    return {'es_empleado': False}