from django.urls import path
from .views import SignUpView, new_usuario, lista_viajes, new_transporte, nuevo_Problema, lista_subastas, lista_subastas_ganadas, lista_transportes, nuevo_Pedido, pedido, lista_pedidos, nuevo_Producto, nuevo_Pago
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('', LoginView.as_view(), name="login" ),
    path('registro/',new_usuario, name="registro"),
    path('registroTransporte/',new_transporte, name="registroTransporte"),
    path('listaTransportes/',lista_transportes, name="listaTransportes"),
    path('nuevoPedido/',nuevo_Pedido,name="nuevoPedido"),
    path('nuevoProducto/',nuevo_Producto, name="nuevoProducto"),
    path('listaPedidos/',lista_pedidos,name="listaPedidos"),
    path('listaSubastas/',lista_subastas,name="listaSubastas"),
    path('listaSubastasGandas/',lista_subastas_ganadas,name="listaSubastasGanadas"),
    path('informarProblema/',lista_pedidos,name="informarProblema"),
    path('listaViajes/',lista_viajes,name="listaViajes"),
    path('confirmarPedido/', lista_pedidos, name="confirmarPedido"),
    path('pago/', nuevo_Pago, name="pago"),
    path('informe/', nuevo_Problema, name="informe"),
]