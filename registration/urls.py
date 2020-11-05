from django.urls import path, re_path
from .views import SignUpView, new_usuario, new_transporte, lista_transportes, nuevo_Pedido, pedido, lista_pedidos, nuevo_Producto, nuevo_Pago, listado_productos
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
    path('confirmarPedido/', lista_pedidos, name="confirmarPedido"),
    path('pago/', nuevo_Pago, name="pago"),
    re_path('', listado_productos, name="listado_productos"),

]