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
    path('user_profile',views.user_profile,name="user_profile"),
    path('user_update/<int:id>',views.user_update,name="user_update"),
    path('user_update/user_updates/<int:id>',views.user_updates,name="user_updates"),
    path("checkout/<int:pid>/", views.checkout, name="checkout_buy"),
    path("wishlist/", views.wishlist_page, name="wishlist_page"),
    path("add_to_wishlist/<int:pid>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/remove/<int:pid>/", views.remove_wishlist, name="remove_wishlist"),
    path("cart/", views.cart_page, name="cart_page"),
    path("cart/add/<int:pid>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:pid>/", views.remove_cart, name="remove_cart"),
    path('product/<int:pid>/', views.product_detail, name='product_detail'),
    path("cart/increase/<int:pid>/", views.increase_qty, name="increase_qty"),
    path("cart/decrease/<int:pid>/", views.decrease_qty, name="decrease_qty"),
    path("search/", views.search_products, name="search_products"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/cancel/<int:order_id>/", views.cancel_order, name="cancel_order"),
    path("payment-success/", views.payment_success, name="payment_success"),

    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
