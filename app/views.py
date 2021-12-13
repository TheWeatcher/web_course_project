"""
Definition of views.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpRequest, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from .models import Blog
from .models import Category, Game
from orders.models import Order, OrderItem
from cart.forms import CartAddGameForm
from django.contrib.auth.models import User
from .models import Comment
from .forms import CommentForm
from .forms import BlogForm, GameForm
from django.views.generic import DetailView, View



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас',
            'year':datetime.now().year,
        }
    )
def links(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Ссылки',
            'message':'Полезные ссылки',
            'year':datetime.now().year,
        }
    )

def registration(request):
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()

            regform.save()
            return redirect('home')
    else:
        regform = UserCreationForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'title':'Регистрация',
            'regform': regform,
            'year': datetime.now().year,
         }
    )


def blog (request):
    posts = Blog.objects.all()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Новости',
            'posts': posts,
            'year':datetime.now().year,
            }
        )


def blogpost(request, parametr):
    
    post_1 = Blog.objects.get(id=parametr) 
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
            comment_f.save()
            
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blogpost.html',
        {
            'title':'Новости',
            'post_1': post_1, 
            'comments': comments,
            'form': form,
            'year':datetime.now().year,
        }
    )   

def newpost(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить отзыв',
            'year': datetime.now().year,
            }
        )


def game_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    games = Game.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        games = games.filter(category=category)
    return render(request, 'app/game_list.html',
                  {'title':'Магазин','category': category, 'categories': categories,
                   'games': games})
   

def game_detail(request, id, slug):
    game = get_object_or_404(Game, id=id, slug=slug, available=True)
    cart_game_form = CartAddGameForm()
    return render(request, 'app/game_detail.html', {'title':'Описание игры','game': game, 'cart_game_form': cart_game_form})

def newgame(request):
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        gameform = GameForm(request.POST, request.FILES)
        if gameform.is_valid():
            game_f = gameform.save(commit=False)
            game_f.created = datetime.now()
            game_f.save()

            return redirect('home')
    else:
        gameform = GameForm()

    return render(
        request,
        'app/newgame.html',
        {
            'gameform': gameform,
            'title': 'Добавить товар',
            'year': datetime.now().year,
            }
        )

def my_orders(request):
    """Renders the about page."""
    
    if Order.objects.filter(nickname=request.user):
        
        game_ordered = OrderItem.objects.filter(order__nickname=request.user)
        assert isinstance(request, HttpRequest)
        return render(
            request,
            'app/my_orders.html', {'title':'Заказы','game_ordered': game_ordered,}
            )
    else:
        return redirect('empty')

def empty(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/empty.html',
        {
            'title':'Корзина',
            'year':datetime.now().year,
        }
    )


def users(request):
    users_list = User.objects.all()
    
    context = {
            "title": "Список пользователей",
            "users_list": users_list,

        }
    return render(request, 'app/users.html', context)

def edit(request, id):
    try:
        user = User.objects.get(id=id)
 
        if request.method == "POST":
            user.is_staff = request.POST.get("is_staff")
            user.save()
            return redirect("users")
        else:
            return render(request, "app/edit.html", {'title':'Извенение пользовател',"user": user})
    except User.DoesNotExist:
        return HttpResponseNotFound("Данного пошльзователя не существует>")

def delete(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return redirect("users")
    except User.DoesNotExist:
        return HttpResponseNotFound("Пользователя не существует")

def edit_order(request, id):
    try:
        order = Order.objects.get(id=id)
 
        if request.method == "POST":
            order.paid = request.POST.get("paid")
            order.save()
            return redirect("orders")
        else:
            return render(request, "app/edit_order.html", {'title':'Изменение статуса заказа',"order": order})
    except Order.DoesNotExist:
        return HttpResponseNotFound("Данного пользователя не существует")

def orders(request):
    """Renders the about page."""

    
    o = Order.objects.all()
    game_ordered = OrderItem.objects.raw('SELECT orders_orderitem.order_id, order_id, game_id, price, created, quantity, orders_order.id,  paid FROM orders_orderitem JOIN orders_order ON orders_orderitem.order_id = orders_order.id')
    assert isinstance(request, HttpRequest)
    return render(request,'app/orders.html', {'title':'Заказы','game_ordered': game_ordered, 'orders': orders,}
            )
