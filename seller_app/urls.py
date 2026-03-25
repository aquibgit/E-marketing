"""
URL configuration for emarketing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('seller_profile',views.seller_profile,name="seller_profile"),
    path('seller_update/<int:id>',views.seller_update,name="seller_update"),
    path('seller_update/seller_updates/<int:id>',views.seller_updates,name="seller_updates"),
    path('seller_update', views.seller_profile, name='seller_update'),
    path('category/<int:cid>/', views.category_products, name='category_products'),
    path("product/<int:pid>/", views.product_details, name="product_details"),
    path("add_product/", views.add_product, name="add_product"),
    path('add_product/add_product_action',views.add_product_action),
    path("seller_products", views.seller_products, name="seller_products"),
    path("seller_orders/", views.seller_orders, name="seller_orders"),
    path("seller_orders/update/<int:order_id>/", views.update_order_status, name="update_order_status"),

    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)