from django.urls import path
from .views import SignUpView, new_usuario, new_transporte, lista_transportes, nuevo_Pedido, pedido, lista_pedidos, nuevo_Producto
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('', LoginView.as_view(), name="login" ),
    path('registro/',new_usuario, name="registro"),
    path('registroTransporte',new_transporte, name="registroTransporte"),
    path('listaTransportes',lista_transportes, name="listaTransportes"),
    path('nuevoPedido',nuevo_Pedido,name="nuevoPedido"),
    path('listaPedidos',lista_pedidos,name="listaPedidos"),
    path('nuevoProducto',nuevo_Producto, name="nuevoProducto")

]