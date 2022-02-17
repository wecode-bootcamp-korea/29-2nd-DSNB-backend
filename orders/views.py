import json

from django.http import JsonResponse
from django.utils import timezone

from orders.models import Order
from users.models import User, UserLibrary, UserWallet

from django.views import View

from orders.utils import CheckOrderValidate as check, OrderUtils as orderutil

class OrderBookView(View):

    @staticmethod
    def write_user_info(self,query_result):
        user_info = list()
        user_info = [
            {
                "user_id"  : user.id,
                "nickname" : user.nickname,
                "email"    : user.email
            }for user in query_result
        ]
        return user_info

    @staticmethod
    def write_order(self,data,order_status):
        try:
            obj, created = Order.objects.update_or_create(
                    user_id          = data['buyer'],
                    target_user_id   = data['target_user'],
                    bookoption_id    = data['book_option'],
                    payment_id       = data['payment_id'],
                    order_status_id  = order_status
                )
        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"},status = 400)

    @check.keyword_validate
    def get(self,request,**kargs):
        keyword = request.GET.get('word', None)
        
        user_email    = User.objects.filter(nickname__contains = keyword).order_by('id')
        user_nickname = User.objects.filter(email__contains = keyword).order_by('id')
        
        result_data           = dict()
        result_data['email']  = self.write_user_info(self,user_nickname)
        result_data['nick']   = self.write_user_info(self,user_email)
        result_data['result'] = 'success'
        
        return JsonResponse(result_data,status = 200)
    
    @check.is_already_have
    def post(self, request):
        try :
            data        = json.loads(request.body)
            book_price  = int(data['price'])
            user_wallet = UserWallet.objects.filter(user_id = data['buyer']).get()
            
            if book_price > user_wallet.cash :
                self.write_order(self, data, 2)
                return JsonResponse({"result" : "fail" , "message" : "low_cash"}, status =201)

            self.write_order(self, data, 1)

            #func (wallet, num)
            orderutil.cash_calc(self, user_wallet, int(-1 * book_price))

            UserLibrary.objects.create(
                user_id  = data['target_user'],
                book_id  = data['book_id'],
                bookmark = 0
            )

            result           = dict()
            result['result'] = "success"
            return JsonResponse(result, status = 201)

        except KeyError :
            return JsonResponse({"message": "KEY_ERROR"},status = 400)
        except UserWallet.DoesNotExist :
            return JsonResponse({"message": "No_CASH"},status = 400)
    
    #validuser 되었다고 가정
    #soft_delete
    def delete(self, request, order_id):
        ##temp : order_id로 user_id 조회, 주문시에만 취소가능
        try :
            result          = dict()
            order           = Order.objects.filter(id = order_id).get()
            order_update    = Order.objects.filter(id = order_id)
            
            if order.user != order.target_user :
                result['result']  = 'fail'
                result['message'] = "GIFT_ORDER_COULDN'T REFUND"
                return JsonResponse(result, status = 200)
            
            user_library = UserLibrary.objects.filter(
                user_id = order.user, 
                book_id = order.bookoption_id.book.id)
            
            if user_library.get().bookmark == 0 and not user_library.get().deleted_at :
                
                user_library.update(deleted_at   = timezone.now())
                order_update.filter(id = order_id).update(order_status = 7)               
                user_wallet = UserWallet.objects.filter(user_id = order.user).get()
                orderutil.cash_calc(self, user_wallet, 1 * (order.bookoption_id.price))
                
                result['result'] = 'success'
                result['message'] = 'refund_complete'
                return JsonResponse(result, status = 200)
            
            if order.order_status.id == 7 :
                result['result'] = 'fail'
                result['message'] = 'already_refund'
                return JsonResponse(result,status=200)
            
            if order.order_status.id <= 6 :
                result['result'] = 'fail'
                result['message'] = 'already_cancel'
                return JsonResponse(result,status=400)
    
            return JsonResponse({'message':'ALREADY_CENCAL'},status = 404)
        except Order.DoesNotExist :
            return JsonResponse({"message": "INVALID_ORDER"}, status = 404)
        except UserLibrary.DoesNotExist : 
            return JsonResponse({"message": "INVALID_ORDER"}, status = 404)