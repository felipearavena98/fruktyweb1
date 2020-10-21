from django.urls import path
from .views import SignUpView, new_usuario, new_transporte, lista_transportes
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name="signup"),
    path('', LoginView.as_view(), name="login" ),
    path('registro/',new_usuario, name="registro"),
    path('registroTransporte',new_transporte, name="registroTransporte"),
    path('listaTransportes',lista_transportes, name="listaTransportes"),

]