from django.db import models
from app.models import Game
from django.contrib.auth.models import User
 
# Create your models here.
 
 
class Order(models.Model):
    nickname= models.ForeignKey(User, on_delete=models.CASCADE, verbose_name = 'Покупатель')
    first_name = models.CharField(max_length=50, verbose_name = 'Фамилия')
    last_name = models.CharField(max_length=50, verbose_name = 'Имя')
    email = models.EmailField(verbose_name = 'E-mail')
    created = models.DateTimeField(auto_now_add=True, verbose_name = 'Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name = 'Изменен')
    paid = models.BooleanField(default=False, verbose_name = 'Оплачен')
    
    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
 
    def __str__(self):
        return 'Order {}'.format(self.id)
 
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
 
 
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', verbose_name = 'Заказ')
    game = models.ForeignKey(Game, related_name='order_items', verbose_name = 'Игра')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name = 'Цена')
    quantity = models.PositiveIntegerField(default=1, verbose_name = 'Количество')
 
    def __str__(self):
        return '{}'.format(self.id)
 
    def get_cost(self):
        return self.price * self.quantity
    class Meta:
        verbose_name = 'Предмет заказа'
        verbose_name_plural = 'Предметы заказа'
 