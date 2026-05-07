from django.shortcuts import render, redirect
from .models import Category, MenuItem, Customer, CartItem, Staff, Order, OrderItem, DutySchedule

# Create your views here.
def home(request):
    categories = Category.objects.all()
    items = MenuItem.objects.all()
    username = request.session.get('customer_name')
    context = {
        'categories': categories,
        'items': items,
        'username': username,
    }
    return render(request, 'index.html', context)

def reg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')

        if Customer.objects.filter(username=uname).exists():
            error = "Username already exists"
            return render(request, 'reg.html', {'error': error})
        
        if Customer.objects.filter(email=email).exists():
            error = "Email already exists"
            return render(request, 'reg.html', {'error': error})

        customer = Customer(name=name, email=email, username=uname, password=pword)
        customer.save()
        return redirect('home')

    return render(request, 'reg.html')
    

def login(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')

        # Check for Admin credentials first
        if uname == 'admin' and pword == 'admin123':
            request.session['is_admin'] = True
            return redirect('admin_dashboard')

        # Check for Staff
        try:
            staff = Staff.objects.get(username=uname, password=pword)
            request.session['staff_id'] = staff.id
            request.session['staff_name'] = staff.name
            return redirect('staff_dashboard')
        except Staff.DoesNotExist:
            pass

        # Otherwise check for Customer
        try:
            customer = Customer.objects.get(username=uname, password=pword)
            request.session['customer_id'] = customer.id
            request.session['customer_name'] = customer.name
            return redirect('customer_home')
        except Customer.DoesNotExist:
            error = "Invalid Username or Password"
            return render(request, 'login.html', {'error': error})

    return render(request, 'login.html')

def logout(request):
    if 'customer_id' in request.session:
        del request.session['customer_id']
    if 'customer_name' in request.session:
        del request.session['customer_name']
    return redirect('home')

def customer_home(request):
    if 'customer_id' not in request.session:
        return redirect('login')
    
    categories = Category.objects.all()
    items = MenuItem.objects.all()
    username = request.session.get('customer_name')
    context = {
        'categories': categories,
        'items': items,
        'username': username,
    }
    return render(request, 'customer_home.html', context)

# --- Admin Dashboard Views ---

# --- Admin Dashboard Views ---

def admin_logout(request):
    if 'is_admin' in request.session:
        del request.session['is_admin']
    return redirect('login')

def admin_dashboard(request):
    if not request.session.get('is_admin'):
        return redirect('login')
    
    categories = Category.objects.all()
    items = MenuItem.objects.all()
    customers = Customer.objects.all()
    staffs = Staff.objects.all()
    duty_schedules = DutySchedule.objects.all()
    
    context = {
        'categories': categories,
        'items': items,
        'customers': customers,
        'staffs': staffs,
        'duty_schedules': duty_schedules,
        'total_items': items.count(),
        'total_categories': categories.count(),
        'total_customers': customers.count(),
    }
    return render(request, 'admin_dashboard.html', context)

# Category CRUD
def add_category(request):
    if not request.session.get('is_admin'):
        return redirect('login')
    if request.method == 'POST':
        name = request.POST.get('name')
        Category.objects.create(name=name)
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

def edit_category(request, id):
    if not request.session.get('is_admin'):
        return redirect('login')
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.save()
        return redirect('admin_dashboard')
    return render(request, 'edit_category.html', {'category': category})

def delete_category(request, id):
    if not request.session.get('is_admin'):
        return redirect('login')
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('admin_dashboard')

# Duty Schedule Assignment
def assign_duty_schedule(request):
    if not request.session.get('is_admin'):
        return redirect('login')
    if request.method == 'POST':
        staff_id = request.POST.get('staff')
        day = request.POST.get('day')
        shift = request.POST.get('shift')
        
        try:
            staff = Staff.objects.get(id=staff_id)
            if shift == 'Morning':
                start_time = '08:00'
                end_time = '16:00'
            else:
                start_time = '16:00'
                end_time = '23:59'
                
            DutySchedule.objects.create(
                staff=staff,
                day=day,
                start_time=start_time,
                end_time=end_time
            )
        except Staff.DoesNotExist:
            pass
            
    return redirect('admin_dashboard')

# MenuItem CRUD
def add_menu_item(request):
    if not request.session.get('is_admin'):
        return redirect('login')
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        cat_id = request.POST.get('category')
        image = request.FILES.get('image')
        
        category = Category.objects.get(id=cat_id)
        MenuItem.objects.create(
            title=title,
            description=description,
            price=price,
            category=category,
            image=image
        )
        return redirect('admin_dashboard')
    return redirect('admin_dashboard')

def edit_menu_item(request, id):
    if not request.session.get('is_admin'):
        return redirect('login')
    item = MenuItem.objects.get(id=id)
    categories = Category.objects.all()
    if request.method == 'POST':
        item.title = request.POST.get('title')
        item.description = request.POST.get('description')
        item.price = request.POST.get('price')
        cat_id = request.POST.get('category')
        item.category = Category.objects.get(id=cat_id)
        
        if request.FILES.get('image'):
            item.image = request.FILES.get('image')
            
        item.save()
        return redirect('admin_dashboard')
    return render(request, 'edit_menu_item.html', {'item': item, 'categories': categories})

def delete_menu_item(request, id):
    if not request.session.get('is_admin'):
        return redirect('login')
    item = MenuItem.objects.get(id=id)
    item.delete()
    return redirect('admin_dashboard')

# --- Cart & Payment Views ---

def item_detail(request, item_id):
    item = MenuItem.objects.get(id=item_id)
    context = {
        'item': item,
        'username': request.session.get('customer_name')
    }
    return render(request, 'item_detail.html', context)

def add_to_cart(request, item_id):
    if 'customer_id' not in request.session:
        return redirect('login')
    
    customer = Customer.objects.get(id=request.session['customer_id'])
    item = MenuItem.objects.get(id=item_id)
    
    quantity = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1
    
    cart_item, created = CartItem.objects.get_or_create(customer=customer, item=item)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
        
    return redirect('view_cart')

def view_cart(request):
    if 'customer_id' not in request.session:
        return redirect('login')
    
    customer = Customer.objects.get(id=request.session['customer_id'])
    cart_items = CartItem.objects.filter(customer=customer)
    
    total = sum(item.item.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total': total,
        'username': request.session.get('customer_name')
    }
    return render(request, 'cart.html', context)

def remove_from_cart(request, item_id):
    if 'customer_id' not in request.session:
        return redirect('login')
    
    customer = Customer.objects.get(id=request.session['customer_id'])
    cart_item = CartItem.objects.get(id=item_id, customer=customer)
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        
    return redirect('view_cart')

def payment_page(request):
    if 'customer_id' not in request.session:
        return redirect('login')
    
    customer = Customer.objects.get(id=request.session['customer_id'])
    cart_items = CartItem.objects.filter(customer=customer)
    total = sum(item.item.price * item.quantity for item in cart_items)
    
    context = {
        'total': total,
        'username': request.session.get('customer_name')
    }
    return render(request, 'payment.html', context)

def checkout(request):
    if 'customer_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST':
        customer = Customer.objects.get(id=request.session['customer_id'])
        cart_items = CartItem.objects.filter(customer=customer)
        
        if cart_items.exists():
            total = sum(item.item.price * item.quantity for item in cart_items)
            order = Order.objects.create(customer=customer, total_amount=total)
            
            for c_item in cart_items:
                OrderItem.objects.create(order=order, item=c_item.item, quantity=c_item.quantity)
                
            cart_items.delete()
            return redirect('customer_home')
            
    return redirect('view_cart')

# --- Staff Views ---
def staff_logout(request):
    if 'staff_id' in request.session:
        del request.session['staff_id']
        if 'staff_name' in request.session:
            del request.session['staff_name']
    return redirect('login')

def staff_dashboard(request):
    if 'staff_id' not in request.session:
        return redirect('login')
    
    categories = Category.objects.all()
    items = MenuItem.objects.all()
    customers = Customer.objects.all()
    orders = Order.objects.all().order_by('-created_at')
    staff = Staff.objects.get(id=request.session['staff_id'])
    duty_schedules = DutySchedule.objects.filter(staff=staff)
    
    context = {
        'username': request.session.get('staff_name'),
        'categories': categories,
        'items': items,
        'customers': customers,
        'orders': orders,
        'duty_schedules': duty_schedules,
        'total_items': items.count(),
        'total_categories': categories.count(),
        'total_customers': customers.count(),
    }
    return render(request, 'staff_dashboard.html', context)

def accept_order(request, order_id):
    if 'staff_id' not in request.session:
        return redirect('login')
    
    order = Order.objects.get(id=order_id)
    order.status = 'Accepted'
    order.save()
    
    return redirect('staff_dashboard')
def staff_reg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        uname = request.POST.get('uname')
        pword = request.POST.get('pword')

        if Staff.objects.filter(username=uname).exists():
            error = "Username already exists"
            return render(request, 'staff_reg.html', {'error': error})
        
        if Staff.objects.filter(email=email).exists():
            error = "Email already exists"
            return render(request, 'staff_reg.html', {'error': error})

        staff = Staff(name=name, email=email, username=uname, password=pword)
        staff.save()
        return redirect('admin_dashboard')

    return render(request, 'staff_reg.html')
