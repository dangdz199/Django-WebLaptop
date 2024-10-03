from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q

from .models import Laptop, Order, OrderItem


def get_or_create_order(user):
    return Order.objects.get_or_create(user=user, completed=False)[0]


def update_cart_item_quantity(order_item, quantity):
    order_item.quantity = max(1, int(quantity))  # Đảm bảo số lượng không nhỏ hơn 1
    order_item.save()


def add_to_cart(request, laptop_id):
    laptop = get_object_or_404(Laptop, pk=laptop_id)
    order = get_or_create_order(request.user)

    # Kiểm tra xem laptop đã có trong giỏ hàng chưa
    order_item, created = OrderItem.objects.get_or_create(order=order, product=laptop)
    if not created:
        # Nếu sản phẩm đã có trong giỏ hàng, tăng số lượng
        order_item.quantity += 1
        order_item.save()

    return redirect('laptop_detail', pk=laptop_id)


def update_cart_item(request, item_id):
    order_item = get_object_or_404(OrderItem, pk=item_id)

    if request.method == "POST":
        quantity = request.POST.get('quantity', 1)
        update_cart_item_quantity(order_item, quantity)

    return redirect('cart')


def remove_cart_item(request, item_id):
    order_item = get_object_or_404(OrderItem, pk=item_id)
    order_item.delete()  # Xóa sản phẩm khỏi giỏ hàng
    return redirect('cart')


def cart_view(request):
    order = get_or_create_order(request.user)
    context = {
        'order': order,
    }
    return render(request, 'products/cart.html', context)


def orders(request):
    order = get_or_create_order(request.user)
    context = {
        'order': order,
    }
    return render(request, 'products/orders.html', context)


def laptop_list(request):
    laptops = Laptop.objects.all()
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

    cart_item_count = 0

    if request.user.is_authenticated:
        order = get_or_create_order(request.user)
        cart_item_count = sum(item.quantity for item in order.items.all())

    return render(request, 'products/laptop_list.html', {
        'laptops': laptops,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_order': sort_order,
        'cart_item_count': cart_item_count,
    })


def laptop_detail(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    cart_item_count = 0

    if request.user.is_authenticated:
        order = get_or_create_order(request.user)
        cart_item_count = sum(item.quantity for item in order.items.all())

    context = {
        'laptop': laptop,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'products/laptop_detail.html', context)


def index(request):
    cart_item_count = 0
    laptops = Laptop.objects.all()

    if request.user.is_authenticated:
        order = get_or_create_order(request.user)
        cart_item_count = sum(item.quantity for item in order.items.all())

    context = {
        'laptops': laptops,
        'cart_item_count': cart_item_count,
    }
    return render(request, 'products/index.html', context)


def about(request):
    cart_item_count = 0

    if request.user.is_authenticated:
        order = get_or_create_order(request.user)
        cart_item_count = sum(item.quantity for item in order.items.all())

    context = {
        'cart_item_count': cart_item_count,
    }
    return render(request, 'products/about.html', context)



def contact(request):
    cart_item_count = 0

    if request.user.is_authenticated:
        order = get_or_create_order(request.user)
        cart_item_count = sum(item.quantity for item in order.items.all())

    context = {
        'cart_item_count': cart_item_count,
    }
    return render(request, 'products/contact.html', context)
