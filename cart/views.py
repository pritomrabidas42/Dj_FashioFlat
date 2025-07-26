from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product, ProductSizeStock
from .models import CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    size = request.POST.get('size')
    quantity = int(request.POST.get('quantity', 1))

    size_stock = ProductSizeStock.objects.filter(product=product, size=size).first()
    if not size_stock or size_stock.stock < quantity:
        messages.error(request, f"{size} size not available or insufficient stock.")
        return redirect('product-detail', pk=product.pk)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        size=size,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    messages.success(request, "Product added to cart.")
    return redirect('cart-view')

@login_required
def view_cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in items)
    return render(request, 'cart/cart.html', {'items': items, 'total': total})
