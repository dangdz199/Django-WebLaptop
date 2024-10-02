from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Laptop, Order, OrderItem


def add_to_cart(request, laptop_id):
    laptop = get_object_or_404(Laptop, pk=laptop_id)
    order, created = Order.objects.get_or_create(user=request.user, completed=False)
    
    # Check if the laptop is already in the order
    order_item, created = OrderItem.objects.get_or_create(order=order, product=laptop)
    if not created:
        # If the item is already in the cart, increase the quantity
        order_item.quantity += 1
        order_item.save()
    
    return redirect('laptop_detail', pk=laptop_id)

def update_cart_item(request, item_id):
    order_item = get_object_or_404(OrderItem, pk=item_id)
    
    if request.method == "POST":
        quantity = request.POST.get('quantity', 1)
        order_item.quantity = max(1, int(quantity))  # Đảm bảo số lượng không nhỏ hơn 1
        order_item.save()
    
    return redirect('cart')

def remove_cart_item(request, item_id):
    order_item = get_object_or_404(OrderItem, pk=item_id)
    order_item.delete()  # Xóa sản phẩm khỏi giỏ hàng
    return redirect('cart')

def cart_view(request):
    order = Order.objects.filter(user=request.user, completed=False).first()
    context = {
        'order': order,
    }
    return render(request, 'products/cart.html', context)

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


