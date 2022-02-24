import random

from django.http      import JsonResponse

from django.db.models import Q, F, Count , Max , Window
from django.db.models.functions import Rank

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
    
    def make_nav_list(self, categories):
        category_list = list()
        category_list = [
            {
                "id"    : category.id,
                "name"  : category.name,
                "url"   : f"books/nation/{category.id}"
            }for category in categories
        ]

        category_list.insert(0, 
            {
                "name" : "전체 보기",
                "url"  : "books/nation"
            }
        )
        return category_list
    
    def get(self, reqeust):
        categories = Category.objects.all()
        
        if categories.count() == 0 :
            return JsonResponse({'message' : 'NO_ASSET'}, status = 404)
        
        result_data = dict()
        result_data['categories'] = self.make_nav_list(categories)
        result_data['result']     = 'success'
        result_data['order']      = [ ## 프론트 요청
            {"name" : "가격 낮은 순" , "keyword" : 'lowprice'},
            {"name" : "가격 높은 순" , "keyword" : 'highprice'},
            {"name" : "출판 순" , "keyword" : 'latest'},
            {"name" : "리뷰 순" , "keyword" : 'review'},
        ]
        return JsonResponse(result_data,status=200)

class BookDetailView(View):
    def calc_discount_price(self, book_option_price , discount_percent):
        return float(book_option_price) * (1 - float(discount_percent) * 0.01)

    def get(self, request, book_id):
        try:
            book  = Book.objects.get(id = book_id)
            author = book.author
            book_options = BookOption.objects.filter(book = book_id)
            books_by_author = Book.objects.filter(author = book.author.id).all()

            result_data = dict()
            author_books = [
                {
                    "book_id"   : book.id,   
                    "title"     : book.title,
                    "img"       : book.cover_image,
                    "rating"    : book.everage_rate,
                    "url"       : f"/books/book/{book.id}"
                }for book in books_by_author
            ]
            result_data['book'] = {
                "book_id"     : book.id,
                "name"        : book.title,
                "img"         : book.cover_image,
                "publisher"   : book.book_detail.publisher,
                "public_date" : book.book_detail.public_date,
		        "rating"      : book.everage_rate,
                "file_url"    : book.file_url,
                "book_option" : [
                    {
                        "id"          : option.id,
                        "name"        : option.option.name,
                        "price"       : float(option.price),
                        "dis_price"   : self.calc_discount_price(option.price, option.discount),
                        "discount"    : option.discount,
                        "is_discount" : option.is_discount
                    }for option in book_options
                ],
                "author" : {
                    "name"  : author.name,
                    "intro" : author.introduction
                }
            }
            result_data['author_write'] = author_books
            result_data['result']       = 'success'
            return JsonResponse(result_data,status=200)

        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"},status=400)

class BookRankView(View):
    def make_rank_list(self, book_rank_list):
        book_rank_dict = [
            {
                "num"          : index + 1,
                "rank"         : rankbook.rank,
                "book_id"      : rankbook.id,
                "title"        : rankbook.title,
                "reveiw_count" : rankbook.review_count
            }for index, rankbook in enumerate(book_rank_list)
        ]
        return book_rank_dict
    
    def get(self, request, **kwargs):
        try:
            rank_books = Book.objects\
                        .annotate(review_count = Count('review_book'))\
                        .annotate(
                            rank = Window(expression=Rank(), order_by = F('review_count').desc()))\
                        .all()[:10]

            result_data          = dict()
            result_data['ranks'] = self.make_rank_list(rank_books)
            
            return JsonResponse(result_data, status=200)

        except Book.DoesNotExist:
            return JsonResponse({"message" : "books_are_not_exists"}, status=404)

class LocationView(View):
    def get(self,request):
        locations = Category.objects.all()
        result = [{
            'id'        : location.id,
            'name'      : location.country,
            'latitude'  : location.latitude,
            'longitude' : location.longitude
        }for location in locations]

        return JsonResponse({'message' : result}, status = 200)

class SlideView(View):
    def get(self,request):
        category  = request.GET.get('category', None)

        books = Book.objects.filter(category_id__country = category).order_by('?')
        result = [{
            'id'       : book.id,
            'title'    : book.title,
            'author'   : book.author.name,
            'category' : book.category.name,
            'image'    : book.cover_image
        }for book in books]
        
        return JsonResponse({
                'message' : 'SUCCESS',
                'result'  : result
            }, status = 200)

class SearchView(View):
    def get(self, request):
        try:
            search = request.GET.get('search')
            books  = Book.objects.filter(Q(title__icontains = search) | Q(author__name__icontains = search))

            result = [{
                'title'  : book.title,
                'author' : book.author.name
            }for book in books]

            return JsonResponse({'message' : 'SUCCESS', 'result' : result})

        except Book.DoesNotExist:
            return JsonResponse({'message' : 'NO_BOOK'}, status = 400)

class BestSellerView(View):
    def get(self, request):
        limit    = int(request.GET.get('limit' , 11))
        offset   = int(request.GET.get('offset', 0))

        books  = Book.objects.all().order_by('?')[offset : offset+limit]

        result = [{
            'id'           : book.id,
            'title'        : book.title,
            'author'       : book.author.name,
            'cover_image'  : book.cover_image,
            'everage_rate' : book.everage_rate,
            'reviews'      : random.randrange(1, 40)
        }for book in books]

        return JsonResponse({'message' : 'SUCCESS', 'result' : result}, status = 200)