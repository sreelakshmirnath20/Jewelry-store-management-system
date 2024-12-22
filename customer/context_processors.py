from account.models import Order,Cart


def item_count(request):
    if request.user.is_authenticated:
        order_count=Order.objects.filter(user=request.user).count()
        cart_count=Cart.objects.filter(user=request.user).count()
        return {"order":order_count,"cart":cart_count}
    
    else:
        return {"order":0,"cart":0}