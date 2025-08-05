from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .utils import get_bkash_token, create_payment, execute_payment
from orders.models import Order
from django.contrib import messages

def bkash_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Get bKash token
    token_response = get_bkash_token()
    id_token = token_response.get('id_token')

    if not id_token:
        return render(request, 'bkash/error.html', {'message': 'Failed to get bKash token'})

    # Create payment request body
    payment_request = {
        "amount": str(order.total_price),
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber": f"inv{order_id}",
        "callbackURL": request.build_absolute_uri(f"/bkash/callback/{order_id}/"),
        "payerReference": str(order.user.id),
    }

    payment_response = create_payment(id_token, payment_request)

    if 'paymentID' in payment_response:
        payment_id = payment_response['paymentID']
        # Save payment_id in session for later use if needed
        request.session['payment_id'] = payment_id
        request.session['id_token'] = id_token
        return render(request, 'bkash/redirect.html', {'paymentID': payment_id, 'order': order})

    return render(request, 'bkash/error.html', {'message': 'Failed to create payment'})

def bkash_callback(request, order_id):
    payment_id = request.GET.get('paymentID') or request.session.get('payment_id')
    id_token = request.session.get('id_token')
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if not payment_id or not id_token:
        messages.error(request, "Payment data missing.")
        return redirect('product_list')

    # Execute payment (finalize)
    execute_response = execute_payment(id_token, payment_id)

    if execute_response.get('transactionStatus') == 'Completed':
        # Update order status here
        order.status = 'Paid'
        order.save()
        messages.success(request, "Payment successful!")
        return redirect('payment_success_page')

    else:
        messages.error(request, "Payment failed or cancelled.")
        return redirect('payment_cancel_page')

def payment_success_page(request):
    return render(request, 'bkash/success.html')

def payment_cancel_page(request):
    return render(request, 'bkash/cancel.html')
