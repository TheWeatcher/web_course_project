from cart.cart import Cart
from django.shortcuts import render
 
from .forms import OrderCreateForm
from .models import OrderItem, Order
from app.models import Game
 
 
# Create your views here.
 
 
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order=form.save(commit=False)
            order.nickname=request.user
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order, game=item['game'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                # clear the cart
            cart.clear()
            return render(request, 'orders/order/created.html',
                          {'title':'Оформление заказа','order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html',
                  {'title':'Оформление заказа', 'cart': cart, 'form': form})

