import json

from django.http import JsonResponse
from django.db.models import Q

from books.models import Book, BookOption, Category

from django.views import View

class BookListView(View) :
    def get(self, request , **kargs):
        try :
            order       = request.GET.get('order', None)
            category_id = kargs.get('category_id') 

            q = Q()
            if category_id != None:
                q.add(Q(category_id = category_id), q.AND)

            books = Book.objects.filter(q).distinct().order_by('-updated_at')
            books= books.select_related('author')

            if order :
                if order == 'lowprice':
                    books = books.order_by('-price')[:20]
                elif order == 'highprice' :
                    books = books.order_by('price')[:20]
                elif order == 'latest' :
                    books = books.order_by('created_at')[:20]
                elif order == 'review' :
                    #리뷰순 -> 추가 구현 내용,후에 추가
                    books = books.order_by('reivew')[:20]
            
            result_data =dict()
            book_list = [{
                "book_id"     : book.id,
                "title"       : book.title,
                "author_name" : book.author.name,
                "img"         : book.cover_image,
                "rating"      : book.everage_rate,
                }for book in books
            ]
            result_data['books']  = book_list
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
        result_data['categories'] = category_list
        result_data['result']     = 'success'
        return JsonResponse(result_data,status=200)

class BookDetailView(View):
    def temp(self, request, **kargs):
        ## 책 디테일 조회
        book_id = kargs.get('book_id')
        
        if book_id == None :
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        book = Book.objects.filter(id = book_id).select_related('book_detail')
        
        if not book.exists():
            return JsonResponse({"message" : "NO_ASSET"}, status=400)        
        
        book_author  = book.select_related('author').get() # 작가 정보
        #print (book_author.author.name)이런 식으로 조회
        book_options = BookOption.objects.filter(book_id = book_id).select_related('option').all()
        #print(book.book_detail.publisher) 이런식으로 조회
        # for option in book_options :
        #     print(f"{option.option.name} :: {option.price}")
        ##작가의 작품 조회
        author_id = book_author.author.id
        
        return JsonResponse({"message": f"{book.book_detail.publisher}"},status=200)

    def get(self, request, **kargs):
        try :
            book_id = kargs.get('book_id')
            
            if book_id == None :
                return JsonResponse({"message" : "KEY_ERROR"}, status=400)
            
            book_data = Book.objects.filter(id = book_id).select_related('book_detail')
            if not book_data.exists() :
                return JsonResponse({"message" : "INVALID_BOOK"}, status=404)

            author_data = book_data.select_related('author').get()
            book_option = BookOption.objects.filter(book_id = book_id).select_related('option').all()
            author_id = author_data.id

            book_data = book_data.get()
            author_write = Book.objects.filter(author_id = author_id).distinct().order_by('-updated_at')[:10]
            
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
                "publisher"   : book_data.book_detail.publisher,
                "public_date" : book_data.book_detail.public_date,
		        "rating"      : book_data.everage_rate,
                "book_option" : [
                    {
                        "id"    : option.id,
                        "name"  : option.option.name,
                        "price" : option.price,
                        "discount" : option.discount,
                        "is_discount" : option.is_discount
                    }for option in book_option
                ],
                "author" : {
                    "name"    : author_data.author.name,
                    "intro"   : author_data.author.introduction
                }
            }
            result_data['author_write'] = author_books
            ##인기순 리뷰순으로 추가
            
            ##file 전송 추가할 부분
            result_data['result']   = 'success'
            return JsonResponse(result_data,status=200)

        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"},status=400)

class MainBookListView(View):
    def get(self, request):
        ##나라순 별로 그룹 지어서 json으로 증가
        ##select * from books group by category_id order by rating DESC:
        return JsonResponse(result,status = 200)