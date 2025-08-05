from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import CartItem
from .models import Address, Order, OrderItem
from products.models import ProductSizeStock

@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect('cart-view')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        street = request.POST.get('street')

        address = Address.objects.create(
            user=request.user,
            full_name=name,
            email=email,
            phone=phone,
            country=country,
            city=city,
            postal_code=postal_code,
            street_address=street
        )

        total_price = sum(item.product.price * item.quantity for item in items)
        order = Order.objects.create(user=request.user, address=address, total_price=total_price)

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                size=item.size,
                quantity=item.quantity,
                price=item.product.price
            )
            stock = ProductSizeStock.objects.get(product=item.product, size=item.size)
            stock.stock -= item.quantity
            stock.save()
            item.delete()

        # ✅ Redirect to bKash payment page
        return redirect('bkash_payment', order_id=order.id)

    return render(request, 'orders/checkout.html', {'items': items})

