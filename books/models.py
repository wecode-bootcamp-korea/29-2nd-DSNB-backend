import uuid

from django.db import models
from core.models import Base

class Category(models.Model) :
    name = models.CharField(max_length=50)
    
    class Meta :
        db_table = 'categories'

class Author(models.Model) :
    name            = models.CharField(max_length=50)
    introduction    = models.CharField(max_length=500, blank= False)

    class Meta :
        db_table = 'authors'

class Book(Base) :
    author      = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    catetory    = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    
    title       = models.CharField(max_length=100, blank=False) 
    publisher   = models.CharField(max_length=200, blank=False)
    public_date = models.DateTimeField(blank=False)
    ISBN        = models.CharField(max_length=15, blank=False)
    intro       = models.CharField(max_length=50, blank=False)

    class Meta :
        db_table = 'books'

class BookFiles(Base) :
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable = False)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, blank = False)
    path = models.CharField(max_length=500)
 
    class Meta :
        db_table = 'book_files'

class BookOptionType (models.Model) :
    name = models.CharField(max_length=30)
    
    class Meta : 
        db_table = 'book_option_types'

class BookOption (models.Model) :
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    option = models.ForeignKey(BookOptionType, on_delete=models.CASCADE, null= True)
    discount = models.PositiveSmallIntegerField(default=0)
    price = models.DecimalField(max_digits = 7, decimal_places = 2)
    is_discount = models.BooleanField(default=False)

    class Meta :
        db_table = 'book_options'