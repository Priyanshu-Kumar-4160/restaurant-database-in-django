from rest_framework import viewsets
from .models import Restaurant, MenuItem, Order, OrderItem
from .serializers import RestaurantSerializer, MenuItemSerializer, OrderSerializer, OrderItemSerializer
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Order, OrderItem, MenuItem
from django.contrib.admin.views.decorators import staff_member_required

def home_view(request):
    return HttpResponse("Home view reached! Template is not the issue.")

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # update this to your main page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def home(request):
    return HttpResponse("Welcome to the Restaurant Management System!")


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer


def home_view(request):
    return render(request, 'home.html')

def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurant_list.html', {'restaurants': restaurants})

def menu_items_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, 'menu_items.html', {'restaurant': restaurant, 'items': items})


@login_required
def add_to_cart(request, item_id):
    item = MenuItem.objects.get(id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=item)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view-cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)
    return render(request, 'cart.html', {'items': items})

@login_required
def place_order(request):
    cart = Cart.objects.get(user=request.user)
    order = Order.objects.create(user=request.user)
    for item in CartItem.objects.filter(cart=cart):
        OrderItem.objects.create(order=order, menu_item=item.menu_item, quantity=item.quantity)
    cart.items.clear()  # empty the cart
    return render(request, 'order_success.html', {'order': order})

from .models import Order

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})


@staff_member_required
def manage_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'manage_orders.html', {'orders': orders})

@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return redirect('manage-orders')

    return render(request, 'update_order_status.html', {'order': order})
