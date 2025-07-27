import requests
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from orders.models import Order 


@csrf_exempt
def initiate_payment(request, order_id):
    order = Order.objects.get(id=order_id)
    amount = order.get_total()  # define this method
    email = order.user.email
    name = request.user.get_full_name()
    phone = getattr(order, 'phone', '01700000000')  # Fallback
    address = getattr(order, 'shipping_address', 'Default Address')
    product_names = ', '.join([item.product.name for item in order.items.all()])

    post_body = {
        'store_id': 'YOUR_STORE_ID',
        'store_passwd': 'YOUR_STORE_PASSWORD',
        'total_amount': amount,
        'currency': 'USD',
        'tran_id': f'FF{order.id}',
        'success_url': request.build_absolute_uri('/payment/success/'),
        'fail_url': request.build_absolute_uri('/payment/fail/'),
        'cancel_url': request.build_absolute_uri('/payment/cancel/'),
        'cus_name': order.user.get_full_name(),
        'cus_name': name,
        'cus_email': email,
        'cus_add1': address,
        'cus_phone': phone,
        'product_name': product_names,
        'product_category': 'Fashion',
    }

    response = requests.post('https://sandbox.sslcommerz.com/gwprocess/v4/api.php', data=post_body)
    data = response.json()

    return redirect(data['GatewayPageURL'])


 # make sure this import is correct

def payment_success(request):
    transaction_id = request.GET.get('tran_id')
    order_id = int(transaction_id.replace('FF', '')) 
    order = Order.objects.get(id=order_id)

    # Mark the order as paid
    order.is_paid = True
    order.transaction_id = transaction_id
    order.save()

    return render(request, 'payments/success.html')


def payment_success(request):
    return render(request, 'payments/success.html')

def payment_fail(request):
    return render(request, 'payments/fail.html')

def payment_cancel(request):
    return render(request, 'payments/cancel.html')

