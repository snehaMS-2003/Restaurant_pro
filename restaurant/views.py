from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Menu, Order
from .forms import MenuForm

# LOGIN
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")

            if user.is_superuser:
                return redirect('admin_page')
            elif user.is_staff:
                return redirect('staff_page')
            else:
                return redirect('customer_page')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


# LOGOUT
def user_logout(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


# REGISTER
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        role = request.POST['role']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        if role == 'admin':
            user = User.objects.create_user(username=username, password=password)
            user.is_superuser = True
            user.is_staff = True
            user.save()

        elif role == 'staff':
            User.objects.create_user(username=username, password=password, is_staff=True)

        else:
            User.objects.create_user(username=username, password=password)

        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'register.html')


# PAGES
@login_required
def admin_page(request):
    return render(request, 'admin_page.html')


@login_required
def staff_page(request):
    return render(request, 'staff_page.html')


@login_required
def customer_page(request):
    return render(request, 'customer_page.html')

# MENU CRUD VIEWS
def menu_list(request):
    items = Menu.objects.all()
    return render(request, 'menu_list.html', {'items': items})

@login_required
def add_menu(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('menu_list')
        
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item added successfully!')
            return redirect('menu_list')
    else:
        form = MenuForm()
    return render(request, 'menu_form.html', {'form': form})

@login_required
def update_menu(request, pk):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('menu_list')
        
    item = get_object_or_404(Menu, id=pk)
    if request.method == 'POST':
        form = MenuForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Menu item updated successfully!')
            return redirect('menu_list')
    else:
        form = MenuForm(instance=item)
    return render(request, 'menu_form.html', {'form': form})

@login_required
def delete_menu(request, pk):
    if not request.user.is_superuser:
        return redirect('menu_list')
        
    item = get_object_or_404(Menu, id=pk)
    item.delete()
    messages.success(request, 'Menu item deleted successfully!')
    return redirect('menu_list')

# UNAVAILABLE FOOD VIEW
@login_required
def unavailable_food(request):
    items = Menu.objects.filter(is_available=False)
    return render(request, 'unavailable_menu.html', {'items': items})

# ORDERS VIEW
@login_required
def order_list(request):
    if request.user.is_staff or request.user.is_superuser:
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
    return render(request, 'orders_list.html', {'orders': orders})

@login_required
def place_order(request):
    if request.method == 'POST':
        item_ids = request.POST.getlist('items')
        
        if not item_ids:
            messages.error(request, "Please select at least one item to order.")
            return redirect('menu_list')
            
        items = Menu.objects.filter(id__in=item_ids)
        
        # Calculate total price
        total_price = sum(item.price for item in items)
        
        # Create order
        order = Order.objects.create(
            user=request.user,
            total_price=total_price,
            status='Pending'
        )
        
        # Add many-to-many items
        order.items.set(items)
        order.save()
        
        messages.success(request, 'Order placed successfully!')
        return redirect('order_list')
        
    return redirect('menu_list')

@login_required
def update_order_status(request, pk):
    if request.method != 'POST':
        return redirect('order_list')
        
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'You do not have permission to update orders.')
        return redirect('order_list')
        
    order = get_object_or_404(Order, id=pk)
    
    if order.status == 'Pending':
        order.status = 'Completed'
    else:
        order.status = 'Pending'
        
    order.save()
    messages.success(request, f'Order #{order.id} marked as {order.status}!')
    return redirect('order_list')