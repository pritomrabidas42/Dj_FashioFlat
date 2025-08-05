from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions

from ..utils import get_bkash_token, create_payment, execute_payment
from orders.models import Order
from ..models import BkashPayment
from .serializers import BkashInitiateSerializer, BkashExecuteSerializer, BkashPaymentSerializer

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bkash_initiate_payment(request):
    serializer = BkashInitiateSerializer(data=request.data)
    if serializer.is_valid():
        order_id = serializer.validated_data['order_id']
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        token_data = get_bkash_token()
        id_token = token_data.get('id_token')

        if not id_token:
            return Response({'error': 'Failed to get bKash token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        payment_request = {
            "amount": str(order.total_price),
            "currency": "BDT",
            "intent": "sale",
            "merchantInvoiceNumber": f"inv{order_id}",
            "callbackURL": f"{request.build_absolute_uri('/')[:-1]}/api/bkash/callback/{order_id}/",
            "payerReference": str(request.user.id),
        }

        payment_response = create_payment(id_token, payment_request)

        if 'paymentID' in payment_response:
            return Response({
                "paymentID": payment_response['paymentID'],
                "bkashURL": payment_response.get('bkashURL'),
                "id_token": id_token
            })

        return Response({'error': 'Failed to create payment.'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bkash_execute_payment(request):
    serializer = BkashExecuteSerializer(data=request.data)
    if serializer.is_valid():
        order_id = serializer.validated_data['order_id']
        payment_id = serializer.validated_data['payment_id']
        id_token = request.headers.get('Authorization')  # Pass as: Authorization: Bearer <id_token>

        if not id_token or not id_token.startswith("Bearer "):
            return Response({'error': 'Missing or invalid Authorization token'}, status=status.HTTP_401_UNAUTHORIZED)

        id_token = id_token.split(" ")[1]

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({'error': 'Order not found.'}, status=status.HTTP_404_NOT_FOUND)

        execute_response = execute_payment(id_token, payment_id)

        if execute_response.get('transactionStatus') == 'Completed':
            # Save BkashPayment
            BkashPayment.objects.create(
                order=order,
                transaction_id=execute_response.get('trxID'),
                phone_number=execute_response.get('customerMsisdn'),
                paid_amount=execute_response.get('amount'),
            )

            order.status = 'Paid'
            order.save()

            return Response({'success': 'Payment completed.'})
        return Response({'error': 'Payment failed or not completed.'}, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_bkash_payment_details(request, order_id):
    try:
        payment = BkashPayment.objects.get(order__id=order_id, order__user=request.user)
    except BkashPayment.DoesNotExist:
        return Response({'error': 'Payment not found.'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BkashPaymentSerializer(payment)
    return Response(serializer.data)
