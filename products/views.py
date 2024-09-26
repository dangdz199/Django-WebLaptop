from django.shortcuts import render, get_object_or_404, redirect
from .models import Laptop
from django.db.models import Q

def add_to_cart(request, laptop_id):
    cart = request.session.get('cart', [])  # Retrieve the cart from session, default to an empty list
    if laptop_id not in cart:
        cart.append(laptop_id)  # Add the laptop to the cart if it's not already there
    request.session['cart'] = cart  # Save the updated cart back to the session
    return redirect('cart')  # Redirect to the cart page


def laptop_list(request):
    laptops = Laptop.objects.all()

    # Lấy các tham số từ form (mặc định là rỗng)
    search_query = request.GET.get('search_query', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    sort_order = request.GET.get('sort_order', '')

    # Bộ lọc tìm kiếm theo tên
    if search_query:
        laptops = laptops.filter(Q(name__icontains=search_query))

    # Bộ lọc giá
    if min_price:
        laptops = laptops.filter(price__gte=min_price)
    if max_price:
        laptops = laptops.filter(price__lte=max_price)

    # Sắp xếp giá
    if sort_order == 'asc':
        laptops = laptops.order_by('price')  # Giá tăng dần
    elif sort_order == 'desc':
        laptops = laptops.order_by('-price')  # Giá giảm dần

    return render(request, 'products/laptop_list.html', {
        'laptops': laptops, 
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_order': sort_order,
    })

def laptop_detail(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    return render(request, 'products/laptop_detail.html', {'laptop': laptop})

def index(request):
    return render(request, 'products/index.html')

def about(request):
    return render(request, 'products/about.html')

def contact(request):
    return render(request, 'products/contact.html')


