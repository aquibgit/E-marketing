from django.shortcuts import render,HttpResponse,redirect
from user_app.models import user_details
from seller_app.models import seller_details,app_seller_detailss
from django.contrib import messages
from emarketing.views import adminindex 
from seller_app.models import Product, Category


# Create your views here.
def reqseller(request):
    data=seller_details.objects.all()
    #response to be sent to html page
    return render(request,'req_seller.html',{'sellers':data})

def Approve_seller(request, id):
    seller_data = seller_details.objects.get(pk=id)
    seller_det = app_seller_detailss(
            name=seller_data.name,
            email=seller_data.email,
            phone=seller_data.phone,
            password=seller_data.password,
            total_sales=0,
            no_of_sales=0    )
    seller_det.save()
    seller_data.delete()
    return redirect(reqseller)

def Delete_seller(request,id):
    seller_data = seller_details.objects.get(pk=id)
    seller_data.delete()
    return redirect(reqseller)

def apseller(request):
    data=app_seller_detailss.objects.all()
    #response to be sent to html page
    return render(request,'vap_seller.html',{'sellers':data})

def Deleteap_seller(request,id):
    seller_data = app_seller_detailss.objects.get(pk=id)
    seller_data.delete()
    return redirect(apseller)

def all_products(request):
    # Fetch all products
    products = Product.objects.all().order_by('-created')  # Latest products first
    categories = Category.objects.all()
    return render(request, 'all_products.html', {'products': products,'categories': categories,})