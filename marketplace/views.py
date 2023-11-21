from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from Medicine_Vendor.models import Vendor
from marketplace.models import Cart
from menu.models import Category, Medicine_lobby
from django.db.models import Prefetch
from .context_processors import get_cart_counter,get_cart_amounts
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.

def marketplace(request):
    vendors = Vendor.objects.filter(is_approved = True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count': vendor_count,
    }
    return render(request, 'marketplace/listings.html',context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)

    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch('Medlist',
                 queryset = Medicine_lobby.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html',context)








def add_to_cart(request, med_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                medlist = Medicine_lobby.objects.get(id=med_id)
                try:
                    chkCart=Cart.objects.get(user=request.user,medlist=medlist)
                    #increase cart quantity
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status':'Success','message':'increased cart quantity','cart_counter': get_cart_counter(request), 'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                except:
                    chkCart=Cart.objects.create(user=request.user, medlist=medlist, quantity=1)
                    return JsonResponse({'status':'Success','message':'Added the med to cart','cart_counter': get_cart_counter(request), 'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'Failed','message':'This med does not exist'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid login'})
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})
    

def decrease_cart(request,med_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                medlist = Medicine_lobby.objects.get(id=med_id)
                try:
                    chkCart=Cart.objects.get(user=request.user,medlist=medlist)
                    if chkCart.quantity>1:
                    #Decrease cart quantity
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    return JsonResponse({'status':'Success','cart_counter': get_cart_counter(request), 'qty':chkCart.quantity,'cart_amount':get_cart_amounts(request)})
                except:
                    return JsonResponse({'status':'Failed','message':'You do not have med to cart'})
            except:
                return JsonResponse({'status':'Failed','message':'This med does not exist'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid login'})
    else:
        return JsonResponse({'status':'login_required','message':'Please login to continue'})

@login_required(login_url = 'login')
def cart(request):
    cart_items=Cart.objects.filter(user=request.user).order_by('created_at')
    context={
        'cart_items':cart_items,
    }
    return render(request, 'marketplace/cart.html',context)

def delete_cart(request,cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                #check if cart item exists
                cart_item = Cart.objects.get(user=request.user,id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status':'Success','message':'Cart item has been deleted','cart_counter': get_cart_counter(request),'cart_amount':get_cart_amounts(request)})
            except:
                return JsonResponse({'status':'Failed','message':'This med does not exist'})
        else:
            return JsonResponse({'status':'Failed','message':'Invalid Request'})


def search(request):
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    med_clc_name = request.GET['med_clc_name']

    
    fetch_vendor_by_medlists = Medicine_lobby.objects.filter(Medicine_title__icontains=med_clc_name,is_available=True).values_list('vendor',flat=True)
    
    vendors =Vendor.objects.filter(Q(id__in=fetch_vendor_by_medlists) | Q(vendor_name__icontains=med_clc_name, is_approved=True, user__is_active=True))

    
    vendor_count = vendors.count()
    context={
        'vendors':vendors,
        'vendor_count':vendor_count,
        'fetch_vendor_by_medlists':fetch_vendor_by_medlists,
    }


    
    return render(request, 'marketplace/listings.html',context) 

