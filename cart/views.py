from django.shortcuts import redirect
from registration.models import Producto
from django.contrib.auth.decorators import login_required
from .cart import Cart
from django.views.generic.base import TemplateView

@login_required(login_url="/accounts/login")
def add_product(request, product_id):
    cart = Cart(request)
    product = Producto.objects.get(id_producto=product_id)
    cart.add(product=product)
    return redirect("listado_productos")


@login_required(login_url="/accounts/login")
def remove_product(request, product_id):
    cart = Cart(request)
    product = Producto.objects.get(id_producto=product_id)
    cart.remove(product)
    return redirect("listado_productos")


@login_required(login_url="/accounts/login")
def decrement_product(request, product_id):
    cart = Cart(request)
    product = Producto.objects.get(id_producto=product_id)
    cart.decrement(product=product)
    return redirect("listado_productos")


@login_required(login_url="/accounts/login")
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("listado_productos")

@login_required(login_url="/accounts/login")
def cart_total_amount(request):
    total = 0.0
    if request.user.is_authenticated:
        for key, value in request.session['cart'].items():
            total = total + (float(value['price']) * value['quantity'])
    return {'cart_total_amount': total}