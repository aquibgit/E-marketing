from django.shortcuts import render,redirect,get_object_or_404
from .models import Product, Category
from seller_app.models import app_seller_detailss
from django.shortcuts import render, redirect
from django.contrib import messages
from seller_app.models import Product
from emarketing.views import sellerindex
from django.db.models import F, Sum
from user_app.models import OrderItem,Order
from seller_app.models import Product


def add_product(request):
    return render(request, "add_product.html")


def add_product_action(request):
    if request.method == "POST":
        name = request.POST.get("name")
        category = request.POST.get("category")
        category_obj, created = Category.objects.get_or_create(name=category)
        price = request.POST.get("price")
        description = request.POST.get("description")
        stock = request.POST.get("stock")
        image = request.FILES.get("image")
        seller_id = request.session.get("sid")
        seller = app_seller_detailss.objects.get(id=seller_id)

        Product.objects.create(
            seller=seller,          
            name=name,
            category=category_obj,
            price=price,
            description=description,
            stock=stock,
            image=image,
        )

        messages.success(request, "Product added successfully!")

    return redirect(sellerindex)

    

# Create your views here.
def seller_profile(request):
    seller_id=request.session['sid']
    seller_data=app_seller_detailss.objects.get(pk=seller_id)
    return render(request,'seller_profile.html',{'result':seller_data})

def seller_update(request,id):
    seller_updt=app_seller_detailss.objects.get(pk=id)
    return render(request,'seller_update.html',{'result':seller_updt})

def seller_updates(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        User_det = app_seller_detailss(id=id, name=name, email=email, phone=phone, password=password)
        User_det.save()
        
        return redirect(seller_profile)
    return render(request, 'seller_update.html')


def category_products(request, cid):
    category = get_object_or_404(Category, id=cid)
    products = Product.objects.filter(category=category)

    return render(request, 'category_products.html', {
        'category': category,
        'products': products
    })

def product_details(request, pid):
    product = get_object_or_404(Product, id=pid)

    return render(request, "product_details.html", {
        "product": product
    })

def seller_products(request):
 
    seller_id = request.session.get("sid")

    seller = app_seller_detailss.objects.get(id=seller_id)

    products = Product.objects.filter(seller=seller)

    return render(request, "seller_products.html", {"products": products})


def seller_orders(request):
    seller_id = request.session.get("sid")
    if not seller_id:
        return redirect('login') 
    seller_products = Product.objects.filter(seller_id=seller_id)

    order_items = OrderItem.objects.filter(product__in=seller_products).annotate(
        total_price=F('price') * F('quantity')
    ).select_related('order', 'product')  

    orders_dict = {}
    for item in order_items:
        order_id = item.order.id
        if order_id not in orders_dict:
            orders_dict[order_id] = {
                "order": item.order,
                "items": [],
                "total_amount": 0
            }
        orders_dict[order_id]["items"].append(item)
        orders_dict[order_id]["total_amount"] += item.total_price

    orders_list = list(orders_dict.values())

    return render(request, "seller_orders.html", {
        "orders_list": orders_list
    })

def update_order_status(request, order_id):
    seller_id = request.session.get("sid")
    if not seller_id:
        messages.error(request, "You must be logged in as a seller.")
        return redirect("login")

    order = get_object_or_404(Order, id=order_id)

    seller_products = Product.objects.filter(seller_id=seller_id)
    if not OrderItem.objects.filter(order=order, product__in=seller_products).exists():
        messages.error(request, "You are not authorized to update this order.")
        return redirect("seller_orders")

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in ["Processing", "Shipped", "Delivered", "Cancelled"]:
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.id} status updated to {new_status}.")
        else:
            messages.error(request, "Invalid status selected.")

    return redirect("seller_orders")