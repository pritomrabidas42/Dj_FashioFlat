from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q , Avg
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, ProductSizeStock, Review
from orders.models import Order

def product_list(request):
    query = request.GET.get('q', '')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    
    if min_rating:
        products = [p for p in products if p.review_set.aggregate(avg=Avg('rating'))['avg'] and p.review_set.aggregate(avg=Avg('rating'))['avg'] >= float(min_rating)]

    context = {
        'pro': products,
        'query': query,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    size_stocks = ProductSizeStock.objects.filter(product=product)
    reviews = product.reviews.filter(is_approved=True)

    # Check if user can review: logged in and purchased & delivered this product
    can_review = False
    if request.user.is_authenticated:
        delivered_orders = Order.objects.filter(user=request.user, status='delivered')
        purchased_products = []
        for order in delivered_orders:
            purchased_products += [item.product.pk for item in order.items.all()]
        if product.pk in purchased_products:
            can_review = True

    context = {
        'product': product,
        'size_stocks': size_stocks,
        'reviews': reviews,
        'can_review': can_review,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def submit_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    # Check if user can review (same logic)
    delivered_orders = Order.objects.filter(user=request.user, status='delivered')
    purchased_products = []
    for order in delivered_orders:
        purchased_products += [item.product.pk for item in order.items.all()]
    if product.pk not in purchased_products:
        messages.error(request, "You can only review products you have purchased and received.")
        return redirect('product-detail', pk=product.pk)

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 0))
        comment = request.POST.get('comment', '').strip()
        if rating < 1 or rating > 5:
            messages.error(request, "Invalid rating.")
            return redirect('product-detail', pk=product.pk)

        # Save review, initially not approved
        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment,
            is_approved=False
        )
        messages.success(request, "Review submitted and awaiting approval.")
        return redirect('product-detail', pk=product.pk)

    return redirect('product-detail', pk=product.pk)
