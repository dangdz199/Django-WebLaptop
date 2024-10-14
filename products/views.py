from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Laptop, Order, OrderItem, UserRegisterForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect đến trang chủ hoặc nơi bạn muốn
        else:
            return render(request, 'products/login.html', {'error': 'Tên đăng nhập hoặc mật khẩu không đúng.'})
    return render(request, 'products/login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tài khoản của bạn đã được tạo thành công! Bạn có thể đăng nhập.')
            return redirect('login')  # Redirect đến trang đăng nhập
        else:
            # Nếu biểu mẫu không hợp lệ, thông báo lỗi cho người dùng
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Lỗi tại {field}: {error}")

    else:
        form = UserRegisterForm()
    
    return render(request, 'products/register.html', {'form': form})

def get_or_create_order(user):
    return Order.objects.get_or_create(user=user, completed=False)[0]

def get_cart_item_count(request):
    cart = request.session.get('cart', {})
    return sum(item['quantity'] for item in cart.values())

def add_to_cart(request, laptop_id):
    laptop = get_object_or_404(Laptop, id=laptop_id)
    cart = request.session.get('cart', {})
    
    if str(laptop.id) in cart:
        cart[str(laptop.id)]['quantity'] += 1
    else:
        cart[str(laptop.id)] = {
            'name': laptop.name,
            'price': str(laptop.price),
            'quantity': 1,
            'image': laptop.image.url,  
        }
    request.session['cart'] = cart
    return redirect('cart')

def view_cart(request):
    cart = request.session.get('cart', {})
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
    
    for item in cart.values():
        item['total'] = float(item['price']) * item['quantity']
    
    return render(request, 'products/cart.html', {'cart': cart, 'total_price': total_price})

def update_cart(request, laptop_id):
    cart = request.session.get('cart', {})
    
    if str(laptop_id) in cart:
        quantity = request.POST.get('quantity', 1)
        if int(quantity) <= 0:
            del cart[str(laptop_id)]
        else:
            cart[str(laptop_id)]['quantity'] = int(quantity)
    
    request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, laptop_id):
    cart = request.session.get('cart', {})
    
    if str(laptop_id) in cart:
        del cart[str(laptop_id)]
    
    request.session['cart'] = cart
    return redirect('cart')


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

    if request.user.is_authenticated:
        order = get_or_create_order(request.user)

    return render(request, 'products/laptop_list.html', {
        'laptops': laptops,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_order': sort_order,
        'cart_item_count': get_cart_item_count(request)

    })

def laptop_detail(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)

    if request.user.is_authenticated:
        order = get_or_create_order(request.user)

    context = {
        'laptop': laptop,
        'cart_item_count': get_cart_item_count(request)
    }
    return render(request, 'products/laptop_detail.html', context)


def index(request):
    cart_item_count = 0
    laptops = Laptop.objects.all()

    if request.user.is_authenticated:
        order = get_or_create_order(request.user)

    context = {
        'laptops': laptops,
        'cart_item_count': get_cart_item_count(request)
    }
    return render(request, 'products/index.html', context)


def about(request):
    cart_item_count = 0

    if request.user.is_authenticated:
        order = get_or_create_order(request.user)

    context = {
        'cart_item_count': get_cart_item_count(request)
    }
    return render(request, 'products/about.html', context)

def contact(request):
    if request.user.is_authenticated:
        order = get_or_create_order(request.user)

    context = {
        'cart_item_count': get_cart_item_count(request)
    }
    return render(request, 'products/contact.html', context)
