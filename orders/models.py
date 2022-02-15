from django.db import models

from core.models  import Base
from books.models import Book
from users.models import User

class OrderStatus(models.Model):
    name = models.CharField(max_length = 20)

    class Meta:
        db_table = 'order_statuses'

class PaymentMethod(models.Model):
    name = models.CharField(max_length = 20)

    class Meta:
        db_table = 'payment_methods'

class Order(Base):
    book_id        = models.ForeignKey(Book, on_delete = models.SET_NULL)
    order_status   = models.ForeignKey(OrderStatus, on_delete = models.SET_NULL)
    target_user_id = models.ForeignKey(User, on_delete = models.SET_NULL)
    user_id        = models.ForeignKey(User, on_delete = models.SET_NULL)
    payment_id     = models.ForeignKey(PaymentMethod, on_delete = models.SET_NULL)
    ordered_at     = models.DateTimeField(auto_now_add = True)
    title          = models.CharField(max_length = 200)
    price          = models.DecimalField(max_digits = 7, decimal_places = 2)
    link_url       = models.CharField(max_length = 250)

    class Meta:
        db_table = 'orders'        