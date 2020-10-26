from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import FormularioLogin, FormularioUsuario, UsuarioForm, TransporteForm, ProcesoForm, BrProductosProcesoForm
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Usuario, Transporte, Producto, ProcesoVenta, BrProductosProcesoDeVenta
from django.contrib.auth import login, logout
from django.views.generic import CreateView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db import connection
import cx_Oracle
from django.contrib.auth.decorators import login_required
import datetime


class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)


class SignUpView(CreateView):
    form_class = FormularioUsuario
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        # Modificar en tiempo real
        return form


def new_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            Usuario = form.save(commit=False)
            Usuario.password = make_password(request.POST['password'])
            Usuario.save()
    else:
        form = UsuarioForm()
    return render(request, 'registration/registro.html', {'form': form})


@login_required(login_url='')
def new_transporte(request):
    if request.method == "POST":
        form = TransporteForm(request.POST)
        if form.is_valid():
            Transporte = form.save(commit=False)
            Transporte.id_cliente = request.user
            Transporte.save()
    else:
        form = TransporteForm()

    return render(request, 'registration/registroTransporte.html', {'form': form})


def lista_transportes(request):
    transportes = Transporte.objects.filter(id_cliente=request.user)
    return render(request, 'registration/listaTransportes.html', {'transportes': transportes})


def pedido(tipo_venta, id_producto, cantidad, id_usuario, fecha):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_agregar_orden_proceso', [
                    tipo_venta, id_producto, cantidad, id_usuario, fecha, salida])
    return salida.getvalue()


def info_pedido(id_pedido):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()
    cursor.callproc('SP_BUSCAR_INFO_PEDIDO', [id_pedido, out_cur])
    lista = []
    for fila in out_cur:
        lista.append(fila)

    return lista


@login_required(login_url='')
def nuevo_Pedido(request):
    productos = Producto.objects.filter(id_estado=1)
    if request.method == 'POST':
        tipo_venta = request.POST.get('comboTipoVenta')
        id_producto = request.POST.get('comboProducto')
        cantidad = request.POST.get('inputCantidad')
        id_usuario = request.user.id_cliente
        fecha = datetime.datetime.now().strftime("%d-%m-%Y")
        salida = pedido(tipo_venta, id_producto, cantidad, id_usuario, fecha)
        mensaje = salida
    else:
        mensaje = ''
    return render(request, 'registration/nuevoPedido.html', {'productos': productos, 'mensaje': mensaje})


def lista_pedidos(request):
    if request.method == 'POST':
        lista = []
        accion = request.POST.get("btnAccion", "")
        if accion == "confirmar":
            id_pedido = request.POST.get("inputId")
            salida = info_pedido(id_pedido)
            for fila in salida:
                if fila[1] == "Interna":
                    coste = fila[7]
                    envio = 6000
                    aduana = 0
                else:
                    coste = fila[7]
                    aduana = int(round(coste * 0.06, 0))
                    envio = 12000
                iva = int(round(coste * 0.19, 0))
                comision = int(round(coste * 0.05, 0))
                servicios = int(round(coste * 0.1, 0))
                total = coste + iva + comision + servicios + aduana + envio
                lista.append(fila)
            return render(request, 'registration/confirmarPedido.html', {'lista': lista, 'iva': iva, 'comision': comision, 'servicios': servicios, 'aduana': aduana, 'envio': envio, 'total': total})

        if accion == "informar":
            id_pedido = request.POST.get("inputId")
    else:
        django_cursor = connection.cursor()
        cursor = django_cursor.connection.cursor()
        out_cur = django_cursor.connection.cursor()
        id_cliente = request.user.pk
        cursor.callproc("SP_LISTAR_PEDIDOS", [id_cliente, out_cur])
        lista = []
        for fila in out_cur:
            lista.append(fila)

    return render(request, 'registration/listaPedidos.html', {'lista': lista})


def producto(nombre, descripcion, cantidad, calidad, formato, precio_unitario, id_usuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_producto_inventario', [
                    nombre, descripcion, cantidad, calidad, formato, precio_unitario, id_usuario, salida])
    return salida.getvalue()


@login_required(login_url='')
def nuevo_Producto(request):
    if request.method == 'POST':
        nombre = request.POST.get('inputNombre')
        descripcion = request.POST.get('inputDescripcion')
        cantidad = request.POST.get('inputCantidad')
        calidad = request.POST.get('comboCalidad')
        formato = request.POST.get('comboFormato')
        precio_unitario = request.POST.get('inputPrecio')
        id_usuario = request.user.id_cliente
        salida = producto(nombre, descripcion, cantidad,
                          calidad, formato, precio_unitario, id_usuario)
        mensaje = salida
    else:
        mensaje = ''
    return render(request, 'registration/nuevoProducto.html', {'mensaje': mensaje})


def pago(id_proceso, iva, monto, cuotas, envio, aduana, servicios, comision):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_pago', [id_proceso, iva, monto,
                                cuotas, envio, aduana, servicios, comision, salida])
    return salida.getvalue()


def nuevo_Pago(request):
    if request.method == 'POST':
        id_proceso = request.POST.get('inputId')
        iva = request.POST.get('inputIva')
        monto = request.POST.get('inputTotal')
        cuotas = request.POST.get('inputCuotas')
        envio = request.POST.get('inputEnvio')
        aduana = request.POST.get('inputAduana')
        servicios = request.POST.get('inputServicios')
        comision = request.POST.get('inputComision')
        salida = pago(id_proceso, iva, monto, cuotas,
                      envio, aduana, servicios, comision)
        mensaje = salida
    else:
        mensaje = ''
    return render(request, 'registration/pago.html', {'mensaje': mensaje})
