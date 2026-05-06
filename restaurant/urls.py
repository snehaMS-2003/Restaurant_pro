from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('admin_page/', views.admin_page, name='admin_page'),
    path('staff_page/', views.staff_page, name='staff_page'),
    path('customer_page/', views.customer_page, name='customer_page'),
    path('logout/', views.user_logout, name='logout'),
    
    # Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html',
        email_template_name='password_reset_email.html'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    
    # Menu & Orders paths
    path('menu/', views.menu_list, name='menu_list'),
    path('add/', views.add_menu, name='add_menu'),
    path('update/<int:pk>/', views.update_menu, name='update_menu'),
    path('delete/<int:pk>/', views.delete_menu, name='delete_menu'),
    path('unavailable/', views.unavailable_food, name='unavailable_food'),
    path('orders/', views.order_list, name='order_list'),
    path('place-order/', views.place_order, name='place_order'),
    path('update-order-status/<int:pk>/', views.update_order_status, name='update_order_status'),
]