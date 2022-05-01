from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from .models import Cart, CartItem
# Create your views here.


def _cartID(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart


def addCart(request, product_id):
    product = Product.objects.get(id=product_id)  # get the product
    try:
        # get the cart ID present in session
        cart = Cart.objects.get(cart_id=_cartID(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cartID(request))

    cart.save()

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        cart_item.save()

    return redirect('show-cart')


def remove_cart(request, product_id):
    cart = Cart.objects.get(cart_id=_cartID(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('show-cart')


def remove_cart_item(request, product_id):
    cart = Cart.objects.get(cart_id=_cartID(request))
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('show-cart')


def showCart(request, total=0, quantity=0, tax=0, grand_total=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cartID(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
    except:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total
    }
    return render(request, 'cart/cart.html', context)
