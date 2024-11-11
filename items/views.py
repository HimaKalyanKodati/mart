from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import RegistrationForm, ProductUploadForm, product_image_set
from .models import *
from django.http import HttpResponse
from django.db.models import Prefetch



# Create your views here.

#home view
def home(request):
    return render(request,'items_temp/index.html')

#logout view
def userlogout(request):
    logout(request)
    return render(request,'items_temp/logout.html')

#signup view
def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'items_temp/registration.html',{'form':form})

def producttype(request, value):
    out = Category.objects.get(name=value)
    #I haven't given a related_name for the model so I have used _set
    #prefetch_related for bulk data/multi-valued relation and select_related for single valued relation
    out_data = out.product_set.prefetch_related('productimage_set')
    return render(request, 'items_temp/data.html', {'out_data':out_data})

@login_required
def productupload(request):    
    if request.method == 'POST':
        product_form = ProductUploadForm(request.POST)
        productimage_form = product_image_set(request.POST, request.FILES)
        if product_form.is_valid() and productimage_form.is_valid():
            product = product_form.save()
            productimage_form.instance = product
            productimage_form.save()
            return redirect('home')
    else:
        product_form = ProductUploadForm()
        productimage_form = product_image_set()
    return render(request, 'items_temp/productform.html',{'product_form':product_form, 'productimage_form':productimage_form})

def product(request, item_id):
    out = Product.objects.get(id=item_id)
    out_data = out.productimage_set.select_related()
    print("Kalyan: ", out)
    print("HIMA: ", out_data)
    return render(request, 'items_temp/product.html', {'out':out,'out_data':out_data})

@login_required
def add_to_cart(request, item_id):
    
    product = get_object_or_404(Product, id=item_id)
    #get_or_create will return tuple that contains data and boolean True or False, if object is created then returns True or viceversa.
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItems.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        #for new products it will be defaults to 1 and same product is added it will add +1
        cart_item.quantity += 1
    else:
        cart_item.price = product.sell_price
    cart_item.save()
    
    try:
        wishlist = WishList.objects.get(product_id = item_id)
        wishlist.delete()
        
    except:
        pass
    
    # return JsonResponse({'data': "Data added successful."})
    return HttpResponse("Success!")

@login_required
def view_cart(request):
    
    # Get the user's cart and related cart items
    cart = Cart.objects.get(user=request.user)# assuming one cart per user
    
    cartitems = CartItems.objects.filter(cart=cart).select_related('product')
    
    # Calculate the total amount by summing the total price of each cart item
    total_amt = sum(item.get_total_price() for item in cartitems)
    
    return render(request, 'items_temp/cart.html', {'cart_item':cartitems, 'total_amt':total_amt})
    
@login_required
def delete_cart(request, item_id):
    cart_item = CartItems.objects.get(id=item_id)
    cart_item.delete()
    
    return redirect('view_cart')

login_required
def add_to_wishlist(request, item_id):
    product = get_object_or_404(Product, id=item_id)
    
    wishlist, created = WishList.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        pass
    else:
        wishlist.description = product.description
        wishlist.price = product.sell_price
    wishlist.save()
    
    return redirect('home')

@login_required
def view_wishlist(request):
    user = User.objects.get(username=request.user)
    
    wishlist = user.wishlist_set.prefetch_related()
    
    return render(request, 'items_temp/wishlist.html', {'wishlist':wishlist})

@login_required
def delete_wishlist(request, item_id):
    wishlist = WishList.objects.get(id=item_id)
    
    wishlist.delete()
    
    return redirect('view_wishlist')


def search(request):
    
    name = request.GET.get('search_name')
    
    if name:
        out_data = Product.objects.filter(name__icontains = name).prefetch_related(Prefetch('productimage_set', queryset=ProductImage.objects.all()))
    
    else:
        out_data = Product.objects.none()
    
    return render(request, 'items_temp/data.html', {'out_data':out_data})
    
    
    