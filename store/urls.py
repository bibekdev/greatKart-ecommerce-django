from django.urls import path
from . import views

urlpatterns = [
    path('', views.showStore, name='show-store'),
    path('category/<slug:category_slug>/',
         views.showStore, name='products-by-category'),
    path('category/<slug:category_slug>/<slug:product_slug>',
         views.productDetail, name='product-detail'),
    path('search/', views.search, name='search'),

]
