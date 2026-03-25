from user_app.models import user_details
from seller_app.models import Product
from .models import Order

from user_app.models import Order   
from django.shortcuts import render, redirect, get_object_or_404
from .models import Wishlist, Cart
from django.db.models import Q
from .decorators import login_required_custom
from .models import OrderItem
from datetime import timedelta
import razorpay
from django.conf import settings
from django.shortcuts import get_object_or_404



def search_products(request):
    query = request.GET.get("q", "")
    
    results = Product.objects.filter(
        Q(name__icontains=query) |
        Q(category__name__icontains=query)
    )

    return render(request, "search.html", {
        "query": query,
        "results": results
    })

def product_detail(request, pid):
    product = get_object_or_404(Product, id=pid)
    return render(request, "product_detail.html", {"product": product})

@login_required_custom
def add_to_wishlist(request, pid):
    uid = request.session.get("uid")
    user = user_details.objects.get(id=uid)
    product = Product.objects.get(id=pid)
    Wishlist.objects.get_or_create(user=user, product=product)
    return redirect("product_detail", pid)

@login_required_custom
def wishlist_page(request):
    user_id = request.session.get("uid")
    user = user_details.objects.get(id=user_id)
    items = Wishlist.objects.filter(user=user)
    return render(request, "wishlist.html", {"items": items})

@login_required_custom
def remove_wishlist(request, pid):
    user_id = request.session.get("uid")
    user = user_details.objects.get(id=user_id)
    Wishlist.objects.filter(user=user, product_id=pid).delete()
    return redirect("wishlist_page")

@login_required_custom
def add_to_cart(request, pid):
    user_id = request.session.get("uid")
    user = user_details.objects.get(id=user_id)
    product = Product.objects.get(id=pid)
    cart_item, created = Cart.objects.get_or_create(
        user=user,
        product=product,
        defaults={"quantity": 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("cart_page")

@login_required_custom
def increase_qty(request, pid):
    user_id = request.session.get("uid")
    user = user_details.objects.get(id=user_id)
    item = Cart.objects.get(user=user, product_id=pid)
    item.quantity += 1
    item.save()
    return redirect("cart_page")

@login_required_custom
def decrease_qty(request, pid):
    user_id = request.session.get("uid")
    user = user_details.objects.get(id=user_id)
    item = Cart.objects.get(user=user, product_id=pid)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete() 

    return redirect("cart_page")

@login_required_custom
def cart_page(request):
    uid = request.session.get("uid")
    user = user_details.objects.get(id=uid)
    cart_items = Cart.objects.filter(user=user)
    total = sum(item.total_price() for item in cart_items)
    return render(request, "cart.html", {"cart_items": cart_items, "total": total})

@login_required_custom
def remove_cart(request, pid):
    uid = request.session.get("uid")
    user = user_details.objects.get(id=uid)
    Cart.objects.filter(user=user, product_id=pid).delete()
    return redirect("cart_page")

@login_required_custom
def buy_product(request, pid):
    product = get_object_or_404(Product, id=pid)

    user_id = request.session.get("uid")
    user = get_object_or_404(user_details, id=user_id)

    order = Order.objects.create(
        user=user,          
        session_id=request.session.session_key or "",  
        full_name=user.name,
        address=user.address,
        phone=user.phone,
        amount=product.price,
        payment_status="SUCCESS",
        status="Processing"
    )
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        price=product.price
    )

    return render(request, "order_success.html", {
        "product": product,
        "order": order
    })

# Create your views here.
def user_profile(request):
    user_id=request.session['uid']
    user_data=user_details.objects.get(pk=user_id)
    return render(request,'user_profile.html',{'result':user_data})

def user_update(request,id):
    user_updt=user_details.objects.get(pk=id)
    return render(request,'user_update.html',{'result':user_updt})

def user_updates(request, id):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        
        User_det = user_details(id=id, name=name, email=email, phone=phone, password=password)
        User_det.save()
        
        return redirect(user_profile)
    return render(request, 'user_update.html')

@login_required_custom
def checkout(request, pid=None):
    uid = request.session.get("uid")
    user = user_details.objects.get(id=uid)

    # CART OR BUY NOW
    if pid:
        product = get_object_or_404(Product, id=pid)
        cart_items = [{'product': product, 'quantity': 1, 'total_price': product.price}]
        total = product.price
    else:
        cart_items = Cart.objects.filter(user=user)
        if not cart_items.exists():
            return redirect("cart_page")
        total = sum(item.total_price() for item in cart_items)

    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")
        phone = request.POST.get("phone")

        # 1️⃣ Create Order in DB (PENDING)
        order = Order.objects.create(
            user=user,
            session_id=request.session.session_key or "",
            full_name=name,
            address=address,
            phone=phone,
            amount=total,
            payment_status="PENDING",
            status="Processing"
        )

        # 2️⃣ Create OrderItems
        if pid:
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1,
                price=product.price
            )
        else:
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart_items.delete()

        # 3️⃣ Razorpay Order Creation
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        razorpay_order = client.order.create({
            "amount": int(total * 100),  # paise
            "currency": "INR",
            "payment_capture": "1"
        })

        # Save Razorpay order id
        order.payment_id = razorpay_order["id"]
        order.save()

        return render(request, "razorpay_checkout.html", {
            "order": order,
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "razorpay_order_id": razorpay_order["id"],
            "amount": total,
            "user": user
        })

    return render(request, "checkout.html", {
        "cart_items": cart_items,
        "total": total,
        "user": user,
    })



def my_orders(request):
    uid = request.session.get("uid")
    user = user_details.objects.get(id=uid)

    orders = Order.objects.filter(user=user).order_by('-created')

    for order in orders:
        if order.status not in ['Delivered', 'Cancelled']:
            order.calculated_delivery = order.created + timedelta(days=7)

    return render(request, "my_orders.html", {"orders": orders})


def cancel_order(request, order_id):
    uid = request.session.get("uid")
    user = user_details.objects.get(id=uid)

    order = get_object_or_404(Order, id=order_id, user=user)

    
    order.status = "Cancelled"
    order.payment_status = "REFUNDED" 
    order.save()
    return redirect("my_orders")

@login_required_custom
def payment_success(request):
    payment_id = request.GET.get("payment_id")

    order = Order.objects.get(payment_id__isnull=False, payment_status="PENDING")
    order.payment_status = "PAID"
    order.payment_id = payment_id
    order.save()
    return redirect("my_orders")

