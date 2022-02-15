from django.db import models

from core.models  import Base
from books.models import Book

class User(Base):
    nickname   = models.CharField(max_length = 20)
    email      = models.CharField(max_length = 250)
    kakao_id   = models.CharField(max_length = 30)
    deleted_at = models.DateTimeField(null = True, default = None)

    class Meta:
        db_table = 'users'

class UserLibrary(Base):
    user_id    = models.ForeignKey(User, on_delete = models.SET_NULL)
    book_id    = models.ForeignKey(Book, on_delete = models.SET_NULL)
    bookmark   = models.PositiveSmallIntegerField()
    deleted_at = models.DateTimeField(null = True, default = None)
 
    class Meta:
        db_table = 'user_libraries'

class UserWallet(Base):
    user_id = models.ForeignKey(User, on_delete = models.SET_NULL)
    cash    = models.DecimalField(max_digits = 7, decimal_places = 2)

    class Meta:
        db_table = 'user_wallets'