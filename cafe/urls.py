"""
URL configuration for cafe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, re_path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('reg/', views.reg, name='reg'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('customer_home/', views.customer_home, name='customer_home'),
    
    # Admin Dashboard
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_logout/', views.admin_logout, name='admin_logout'),
    path('add_category/', views.add_category, name='add_category'),
    path('edit_category/<int:id>/', views.edit_category, name='edit_category'),
    path('delete_category/<int:id>/', views.delete_category, name='delete_category'),
    path('assign_duty/', views.assign_duty_schedule, name='assign_duty_schedule'),
    path('add_menu_item/', views.add_menu_item, name='add_menu_item'),
    path('edit_menu_item/<int:id>/', views.edit_menu_item, name='edit_menu_item'),
    path('delete_menu_item/<int:id>/', views.delete_menu_item, name='delete_menu_item'),

    # Cart & Items
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('payment/', views.payment, name='payment'),
    path('checkout/', views.checkout, name='checkout'),

    # Staff Views
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff_logout/', views.staff_logout, name='staff_logout'),
    path('staff_reg/', views.staff_reg, name='staff_reg'), # New staff registration route
    path('accept_order/<int:order_id>/', views.accept_order, name='accept_order'),
    path('fix-my-login-now/', views.force_admin_access),
]

# Absolute fallback for file serving
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# If static() fails, these will catch it
urlpatterns += [
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
