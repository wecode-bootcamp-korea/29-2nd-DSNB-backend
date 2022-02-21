from django.db import models

from core.models  import Base
from users.models import User
from books.models import Book

class Review(Base):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer')
    book       = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='review_book')
    comment    = models.CharField(max_length=600)
    rating     = models.DecimalField(max_digits = 3, decimal_places = 2)
    is_spoiler = models.BooleanField(default = False)
    
    class Meta:
        db_table = 'reviews'