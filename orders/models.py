from django.db import models

from core.models  import Base
from books.models import BookOption
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
    bookoption_id  = models.ForeignKey(BookOption, on_delete = models.CASCADE)
    order_status   = models.ForeignKey(OrderStatus, on_delete = models.CASCADE)
    target_user    = models.ForeignKey(User, on_delete = models.CASCADE, related_name='target_user')
    user           = models.ForeignKey(User, on_delete = models.CASCADE, related_name='origin_user')
    payment        = models.ForeignKey(PaymentMethod, on_delete = models.CASCADE, related_name='payment')
    ordered_at     = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'orders'