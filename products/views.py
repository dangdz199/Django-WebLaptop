from django.shortcuts import render, get_object_or_404
from .models import Laptop

def laptop_list(request):
    laptops = Laptop.objects.all()
    return render(request, 'products/laptop_list.html', {'laptops': laptops})

def laptop_detail(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    return render(request, 'products/laptop_detail.html', {'laptop': laptop})
