import json

from django.http import JsonResponse
from django.db.models import Q

from books.models import Book

from django.views import View

class BookListView(View) :

    def get(self, request , **kargs):
        try :
            order       = request.GET.get('order', None)
            category_id = kargs.get('category_id') 

            q = Q()
            if category_id != None:
                q.add(Q(catetory_id = category_id), q.AND)

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
                "title"       : book.tilte,
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