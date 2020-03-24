from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from products.models import Product
from django.contrib import auth, messages
from cart.models import Cart, CartItem


def view_cart(request):
    """A View that renders the cart contents page"""
    return render(request, "cart.html") 


def add_to_cart(request, id):
    """Add a quantity of the specified product to the cart"""
    quantity = int(request.POST.get('quantity') or 1)

    product = Product.objects.get(id= id)
    if quantity > product.quantity:
        messages.error(request, f"Only {product.quantity} availible")
        
        return redirect(reverse('index'))

    cart = request.session.get('cart', {})

    if not cart.get(id):
        cart[id] = cart.get(id, quantity)
    else:
        cart[id] += quantity

    request.session['cart'] = cart
    total = round(float(product.price) * quantity, 2)
    if request.session.get("total") :
        request.session["total"] += total

    else: 
        request.session["total"] = total
    if request.user:
        user_cart, created=Cart.objects.get_or_create(user=request.user)
        item=CartItem.objects.filter(cart=user_cart, product_id=id).first()
        if item:
            item.quntity=cart[id]
            item.save()
        else:
            CartItem.objects.create(cart=user_cart, product_id=id, quantity=cart[id])

    return redirect(reverse('products'))



def adjust_cart(request, id):
    """
    Adjust the quantity of the specified product to the specified
    amount
    """
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})

    previous_quantity=cart[id]
    if quantity > 0:
        cart[id] = quantity
    else:
        cart.pop(id)
        
    
    request.session['cart'] = cart
    product = Product.objects.get(id= id)
    if quantity > product.quantity:
        messages.error(request, f"Only {product.quantity} availible")
        
        return redirect(reverse('view_cart'))
    total = round(float(product.price) * quantity, 2)
    if request.session.get("total") :
        request.session["total"] += total
        request.session['total'] -= round(float(product.price) *  previous_quantity, 2)
    else: 
        request.session["total"] = total
    if request.user:
        cart, created=Cart.objects.get_or_create(user=request.user)
        item=CartItem.objects.filter(cart=cart, product_id=id).first()
        if item:
            item.quntity=cart[id]
            item.save()
        else:
            CartItem.objects.create(cart=cart, product_id=id, quntity=cart[id])
    return redirect(reverse('view_cart'))