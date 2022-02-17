import json
import re

from django.http import JsonResponse

from users.models import UserLibrary

from django.db.models import Q, F

class CheckOrderValidate():
    
    LEASTWORD = r'\w{2}'

    def keyword_validate(func):
        def wrapper(self, request,**kargs):
            mode    = request.GET.get('type', None)
            keyword = request.GET.get('word', None)
        
            if mode != 'gift' or mode == None :
                return JsonResponse({"message" : 'INVALID_ORDER_TYPE'},status = 400)
            if not re.fullmatch(self.LEASTWORD, keyword) :
                return JsonResponse({"message" : 'INVALID_WORD_RANGE'},status = 400)
            
            return func(self, request, **kargs)
        return wrapper

    def is_already_have(func):
        def wrapper(self,request):
                try :
                    data = json.loads(request.body)

                    q = Q()
                    q.add(Q(user_id = data['target_user']), q.AND)
                    q.add(Q(book_id = data['book_id']), q.AND)

                    if UserLibrary.objects.filter(q).exists():
                        return JsonResponse({"message" : 'ALREADY_HAVE'},status = 400)
                    return func(self, request)
                except json.JSONDecodeError:
                    return JsonResponse({"message" : 'INVALID_BODY'},status = 400)
                except KeyError:
                    return JsonResponse({"message" : 'KEY_ERROR'},status = 400)
        return wrapper

class OrderUtils():
    def cash_calc(self, user_wallet, book_price):
        user_wallet.cash = F('cash') + book_price
        user_wallet.save()