from django.shortcuts import render,HttpResponse,redirect
from user_app.models import user_details
from seller_app.models import seller_details,app_seller_detailss
from seller_app.models import Category
from django.contrib import messages
from django.db.models import Sum, Count
from user_app.models import OrderItem,Order
from seller_app.models import Product
from django.db.models import Count
import random
from django.utils import timezone
from django.db.models import F, Sum
from django.db.models.functions import TruncDate
from user_app.models import user_details, Order, OrderItem
from seller_app.models import Category

# Create your views here.
def index(request):
    categories = Category.objects.all()
    products = list(Product.objects.all())
    random.shuffle(products)
    featured = products[:20]
    return render(request,'index.html',{"categories": categories,"products": featured,
        "categories": Category.objects.all()})

def sellerindex(request):
    seller_id = request.session.get("sid")
    seller_products = Product.objects.filter(seller_id=seller_id)
    sales_items = OrderItem.objects.filter(product__in=seller_products,order__payment_status="PAID").annotate(total_price=F('price') * F('quantity'))
    total_units = sales_items.aggregate(units=Sum('quantity'))['units'] or 0
    total_revenue = sales_items.aggregate(total=Sum('total_price'))['total'] or 0
    today = timezone.localdate()
    today_revenue = sales_items.filter(order__created__date=today).aggregate(
                revenue=Sum('total_price')
            )['revenue'] or 0
    product_sales = sales_items.values("product__name").annotate(
                units=Sum("quantity"),
                revenue=Sum('total_price')
            ).order_by('-revenue')
    total_sales = sales_items.count()
    return render(request,'seller_index.html', {
                "total_sales": total_sales,
                "total_units": total_units,
                "today_revenue": today_revenue,
                "total_revenue": total_revenue,
                "product_sales": product_sales
            })

def adminindex(request):
    total_revenue = Order.objects.filter(payment_status="PAID").aggregate(total=Sum("amount"))["total"] or 0
    top_seller = (OrderItem.objects.filter(order__payment_status="PAID").values("product__seller__name").annotate(revenue=Sum(F("quantity") * F("price"))).order_by("-revenue")[:5])
    top_products = (OrderItem.objects.filter(order__payment_status="PAID").values("product__name","product__seller__name").annotate(units_sold=Sum("quantity"),revenue=Sum(F("quantity") * F("price"))).order_by("-units_sold")[:5])
    today = timezone.localdate()
    total_orders = OrderItem.objects.filter(order__payment_status="PAID",order__created__date=today).aggregate(total=Sum("quantity"))["total"] or 0
    no_of_sellers = app_seller_detailss.objects.count()
    return render(request,'admin_index.html',{
                "total_revenue": total_revenue,
                "top_seller": top_seller,
                "top_products": top_products,
                "no_of_sellers": no_of_sellers,
                "total_orders": total_orders
            })

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # --- ADMIN LOGIN ---
        if email == 'admin@gmail.com' and password == '123':
            request.session['email'] = email
            request.session['admin'] = 'admin'
            total_revenue = Order.objects.filter(payment_status="PAID").aggregate(total=Sum("amount"))["total"] or 0
            top_seller = (OrderItem.objects.filter(order__payment_status="PAID").values("product__seller__name").annotate(revenue=Sum(F("quantity") * F("price"))).order_by("-revenue")[:5])
            top_products = (OrderItem.objects.filter(order__payment_status="PAID").values("product__name","product__seller__name").annotate(units_sold=Sum("quantity"),revenue=Sum(F("quantity") * F("price"))).order_by("-units_sold")[:5])
            today = timezone.localdate()
            total_orders = OrderItem.objects.filter(order__payment_status="PAID",order__created__date=today).aggregate(total=Sum("quantity"))["total"] or 0
            no_of_sellers = app_seller_detailss.objects.count()

            return render(request, 'admin_index.html', {
                "total_revenue": total_revenue,
                "top_seller": top_seller,
                "top_products": top_products,
                "no_of_sellers": no_of_sellers,
                "total_orders": total_orders
            })

        # --- USER LOGIN ---
        elif user_details.objects.filter(email=email, password=password).exists():
            userdetails = user_details.objects.get(email=email, password=password)
            request.session['uid'] = userdetails.id
            request.session['uname'] = userdetails.name
            request.session['uemail'] = userdetails.email
            request.session['user'] = 'user'
            messages.success(request, "User login successful")

            categories = Category.objects.all()
            products = list(Product.objects.all())
            import random
            random.shuffle(products)
            featured = products[:20]

            return render(request, 'index.html', {
                "categories": categories,
                "products": featured
            })

        # --- SELLER LOGIN ---
        
        elif app_seller_detailss.objects.filter(email=email, password=password).exists():
            sellerdetails = app_seller_detailss.objects.get(email=email, password=password)
            request.session['sid'] = sellerdetails.id
            request.session['sname'] = sellerdetails.name
            request.session['semail'] = sellerdetails.email
            request.session['seller'] = 'seller'
            messages.success(request, "Seller login successful")

            seller_id = request.session.get("sid")
            seller_products = Product.objects.filter(seller_id=seller_id)
            sales_items = OrderItem.objects.filter(product__in=seller_products,order__payment_status="PAID").annotate(total_price=F('price') * F('quantity'))
            total_units = sales_items.aggregate(units=Sum('quantity'))['units'] or 0
            total_revenue = sales_items.aggregate(total=Sum('total_price'))['total'] or 0
            today = timezone.localdate()
            today_revenue = sales_items.filter(order__created__date=today).aggregate(
                revenue=Sum('total_price')
            )['revenue'] or 0
            product_sales = sales_items.values("product__name").annotate(
                units=Sum("quantity"),
                revenue=Sum('total_price')
            ).order_by('-revenue')
            total_sales = sales_items.count()

            return render(request, 'seller_index.html', {
                "total_sales": total_sales,
                "total_units": total_units,
                "today_revenue": today_revenue,
                "total_revenue": total_revenue,
                "product_sales": product_sales
            })


        else:
            messages.error(request, "Login unsuccessful. Invalid credentials.")

    return render(request, 'login.html')


def register(request):
    return render(request,'register.html')

def seller_register(request):
    return render(request,'seller_register.html')

def registeraction(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        if user_details.objects.filter(email=email).exists():
            messages.error(request, "user already exist")
            return render(request,'register.html')
            
        else:
            User_det=user_details(name=name,email=email,phone=phone,password=password)
            User_det.save()
            messages.error(request, "registered successfully")
    return redirect(login)

def seller_registeraction(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        password=request.POST.get('password')
        if seller_details.objects.filter(email=email).exists():
            messages.error(request, "user already exist")
            return render(request,'register.html')
            
        else:
            seller_det=seller_details(name=name,email=email,phone=phone,password=password)
            seller_det.save()
            messages.error(request, "registered successfully")
    return redirect(login)

def logout(request):
     session_key = list(request.session.keys())
     for key in session_key:
          del request.session[key]
     messages.error(request, "logout successful")
     return redirect(index)