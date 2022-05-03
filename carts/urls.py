from django.urls import path
from . import views

urlpatterns = [
    path('', views.showCart, name='show-cart'),
    path('add-cart/<int:product_id>/', views.addCart, name='add-cart'),
    path('remove-cart/<int:product_id>/<int:cart_item_id>/',
         views.remove_cart, name='remove-cart'),
    path('remove-cart-item/<int:product_id>/<int:cart_item_id>/',
         views.remove_cart_item, name='remove-cart-item'),

]
