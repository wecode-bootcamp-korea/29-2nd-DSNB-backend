import json

from django.http      import JsonResponse
from django.db.models import Q, Count , Max

from books.models   import Book, BookOption, Category
from django.views   import View

class BookListView(View):
    
    def make_booklist(self, book_objects):
        book_list = [{
                "book_id"      : book.id,
                "title"        : book.title,
                "author_name"  : book.author.name,
                "img"          : book.cover_image,
                "rating"       : book.everage_rate,
                "review_count" : book.review_count,
                "max_price"    : book.book_price
                }for book in book_objects
            ]
        return book_list

    def get(self, request, **kwargs):
        try :
            order       = request.GET.get('order', 'updated_at')
            category_id = kwargs.get('category_id') 

            q = Q()
            
            if category_id:
                q &= Q(category_id = category_id)
            
            sort = {
                'lowprice'   : 'book_price',
                'highprice'  : '-book_price',
                'latest'     : 'created_at',
                'review'     : 'review_count',
                'updated_at' : '-updated_at'
            }

            books = Book.objects.filter(q).\
                        distinct().\
                        annotate(review_count = Count('review_book'), book_price =  Max('book_option__price')).\
                        order_by(sort[order]).\
                        select_related('author')[:20]
            
            result_data           = dict()
            result_data['books']  = self.make_booklist(books)
            result_data['result'] = 'success'

            return JsonResponse(result_data, status = 200)
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"},status = 400)

class NavCategoryView(View):
    def get(self, reqeust):
        categories  = Category.objects.all()
        
        if categories.count() == 0 :
            return JsonResponse({'message' :  'NO_ASSET'}, status = 404)
        
        result_data   = dict()
        category_list = [
            {
                "id"    : category.id,
                "name"  : category.name,
                "url"   : f"books/{category.id}"
            }for category in categories
        ]

        category_list.insert(0, 
            {
                "name" : "전체 보기",
                "url"  : "books"
            }
        )
        result_data['categories'] = category_list
        result_data['result']     = 'success'
        return JsonResponse(result_data,status=200)

class BookDetailView(View):
    def get(self, request, **kwargs):
        try :
            book_id     = kwargs.get('book_id', None)
            
            book_data   = Book.objects.filter(id = book_id).\
                        select_related('book_detail')
            author_data = book_data.\
                        select_related('author').get()
            
            if not book_data.exists():
                return JsonResponse({"message" : "INVALID_BOOK"}, status=404)
            
            book_options = BookOption.objects.filter(book_id = book_id).\
                            select_related('option')\
                            .all()

            author_write = Book.objects.filter(author_id = author_data.id).\
                            distinct().\
                            order_by('-updated_at')[:10]
            book_data    = book_data.get()

            result_data = dict()
            author_books = [
                {
                    "book_id"   : book.id,   
                    "title"     : book.title,
                    "img"       : book.cover_image,
                    "rating"    : book.everage_rate,
                    "url"       : f"/books/book/{book.id}"
                }for book in author_write
            ]
            result_data['book'] = {
                "name"        : book_data.title,
                "img"         : book_data.cover_image,
                "publisher"   : book_data.book_detail.publisher,
                "public_date" : book_data.book_detail.public_date,
		        "rating"      : book_data.everage_rate,
                "file_url"    : book_data.file_url,
                "book_option" : [
                    {
                        "id"          : option.id,
                        "name"        : option.option.name,
                        "price"       : option.price,
                        "dis_price"   : float(option.price) * (float(option.discount) * (1 - 0.01)),
                        "discount"    : option.discount,
                        "is_discount" : option.is_discount
                    }for option in book_options
                ],
                "author" : {
                    "name"    : author_data.author.name,
                    "intro"   : author_data.author.introduction
                }
            }
            result_data['author_write'] = author_books
            result_data['result']       = 'success'
            return JsonResponse(result_data,status=200)
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"},status=400)