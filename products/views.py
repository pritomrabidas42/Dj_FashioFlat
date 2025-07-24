from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Review
from orders.models import Order
from .forms import ReviewForm
from orders.forms import PurchaseForm
from orders.models import OrderItem 

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

@login_required
def purchase_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            size = form.cleaned_data['size']
            quantity = form.cleaned_data['quantity']
            Order.objects.create(user=request.user, product=product, size=size, quantity=quantity)
            return redirect('product_detail', pk=pk)
    return redirect('products/product_detail', pk=pk)

def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = product.reviews.all().order_by('-created_at')
    review_form = ReviewForm()
    purchase_form = PurchaseForm()

    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    has_purchased = False
    if request.user.is_authenticated:
        # ✅ FIXED: check purchase using OrderItem
        has_purchased = OrderItem.objects.filter(
            product=product,
            order__user=request.user,
            order__complete=True
        ).exists()

        if request.method == 'POST' and 'review_submit' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid() and has_purchased:
                review = review_form.save(commit=False)
                review.user = request.user
                review.product = product
                review.save()
                return redirect('products/product_detail', pk=pk)

    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'review_form': review_form,
        'purchase_form': purchase_form,
        'has_purchased': has_purchased,
        'related_products': related_products,
    })

