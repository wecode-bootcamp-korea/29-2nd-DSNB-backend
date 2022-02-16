from django.db import models

from core.models  import Base
from users.models import User
from books.models import Book

class Review(Base):
    user_id    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer')
    book_id    = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book')
    comment    = models.CharField(max_length=600)
    rating     = models.DecimalField(max_digits = 3, decimal_places = 2)
    is_spoiler = models.BooleanField(default=0)
    
    class Meta:
        db_table = 'reviews'