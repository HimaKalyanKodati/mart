from django.urls import path
from .views import home, java, userlogout, registration, producttype, productupload, product, add_to_cart, view_cart, delete_cart, add_to_wishlist, view_wishlist, delete_wishlist, search
from django.contrib.auth import urls
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
#importing setting
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home, name='home'),
    path('login/', LoginView.as_view(template_name='items_temp/login.html'), name='login'),
    path('logout/', userlogout, name='logout'),
    path('password_reset/', PasswordResetView.as_view(template_name='items_temp/passreset.html'), name='passreset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='items_temp/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='items_temp/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name='items_temp/password_reset_complete.html'), name='password_reset_complete'),
    path('signup/', registration, name='sigup'),
    path('producttype/<str:value>', producttype, name='producttype'),
    path('productupload/',productupload, name='productupload'),
    path('product/<int:item_id>', product, name='product'),
    path('cart/add_to_cart/<int:item_id>', add_to_cart, name='add_to_cart'),
    path('cart/view_cart/', view_cart, name='view_cart'),
    path('cart/delete/<int:item_id>', delete_cart, name='delete_cart'),
    path('wishlist/add_to_wishlist/<int:item_id>', add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/view_wishlist/', view_wishlist, name='view_wishlist'),
    path('wishlist/delete/<int:item_id>', delete_wishlist, name='delete_wishlist'),
    path('search/', search, name='search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
