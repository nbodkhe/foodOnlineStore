from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from marketplace.models import Cart
from menu.models import Category, FoodItem
from vendor.models import Vendor


# Create your views here.


def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors': vendors,
        'vendor_count': vendor_count
    }
    return render(request, 'marketplace/listings.html', context)


def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )
    context = {
        'vendor_slug': vendor_slug,
        'vendor': vendor,
        'categories': categories
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if user has already added food item to the cart
                try:
                    chkcart = Cart.objects.get(user=request.user)
                    # Increase the cart quantity
                    chkcart.quantity += 1
                    chkcart.save()
                    JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity'})
                except:
                    chkcart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    JsonResponse({'status': 'Success', 'message': 'Added the food to the cart'})
            except:
                JsonResponse({'status': 'Failed', 'message': 'This food Does not exist'})
        else:
            JsonResponse({'status': 'Failed', 'message': 'Invalid Request'})
    else:
        return JsonResponse({'status': 'Failed', 'message': 'Please login to continue'})
