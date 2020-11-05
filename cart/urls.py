from django.urls import path, re_path
from .views import add_product, remove_product, decrement_product, clear_cart, cart_total_amount

app_name = "cart"

urlpatterns = [
    path('add_product/<int:product_id>/', add_product, name='add_product'),
    path('remove_product/<int:product_id>/', remove_product, name='remove_product'),
    path('decrement_product/<int:product_id>/', decrement_product, name='decrement_product'),
    path('clear/', clear_cart, name='clear_cart'),
    path('', cart_total_amount, name='cart_total_amount'),

]
