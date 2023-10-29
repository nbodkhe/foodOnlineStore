from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

from marketplace.context_processors import get_cart_counter, get_cart_amount
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
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'vendor_slug': vendor_slug,
        'vendor': vendor,
        'categories': categories,
        'cart_items': cart_items,
    }
    return render(request, 'marketplace/vendor_detail.html', context)


def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if user has already added food item to the cart
                try:
                    chkcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    # Increase the cart quantity
                    chkcart.quantity += 1
                    chkcart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the cart quantity',
                                         'cart_counter': get_cart_counter(request), 'qty': chkcart.quantity,
                                         'cart_amount': get_cart_amount(request)})
                except:
                    chkcart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Added the food to the cart',
                                         'cart_counter': get_cart_counter(request), 'qty': chkcart.quantity, 'cart_amount': get_cart_amount(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food Does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # check the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                # check if user has already added food item to the cart
                try:
                    chkcart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkcart.quantity > 1:
                        # Decrease the cart quantity
                        chkcart.quantity -= 1
                        chkcart.save()
                        qty = chkcart.quantity
                    else:
                        chkcart.delete()
                        qty = 0
                    return JsonResponse({'status': 'Success',
                                         'cart_counter': get_cart_counter(request), 'qty': qty, 'cart_amount': get_cart_amount(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have the item in your cart!'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'This food Does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Please login to continue'})


@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')

    context = {
        'cart_items': cart_items
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                # check if cart items exists
                # cart_items = Cart.objects.get(request.user, id=cart_id)
                cart_items = Cart.objects.get(user=request.user, id=cart_id)
                if cart_items:
                    cart_items.delete()
                    return JsonResponse({'status': 'Success', 'message': 'Cart item has been deleted',
                                         'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amount(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart item does not exist'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Invalid Request'})
