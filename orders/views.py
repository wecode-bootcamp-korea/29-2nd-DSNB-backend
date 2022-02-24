import json

from django.http   import JsonResponse
from django.views  import View

from books.models  import BookOption
from orders.models import Order
from users.models  import UserWallet, UserLibrary

from users.utils   import login_required

class BeforeBuyView(View):
    @login_required
    def get(self, request):
        user    = request.user
        wallets = UserWallet.objects.filter(user_id = user)
        result = [{
            'cash' : float(wallet.cash)
        }for wallet in wallets]
        
        return JsonResponse({'message' : 'SUCCESS' , 'result' : result}, status = 200)

class BuyBookView(View):
    @login_required
    def post(self, request):
        try:
            user = request.user
            current_cash = UserWallet.objects.get(user_id = user)
            data = json.loads(request.body)

            if data['price'] > current_cash.cash:
                return JsonResponse({"result" : "FAILED" , "message" : "LOW_CASH"}, status = 400)

            Order.objects.create(
                user_id         = request.user.id,
                target_user_id  = request.user.id,
                order_status_id = 1,
                payment_id      = 1,
                bookoption_id   = data['book_option'],
            )

            UserLibrary.objects.create(
                user_id  = request.user.id,
                book_id  = data['book_id'],
                bookmark = 1
            )

            return JsonResponse({'message' : 'SUCCESS'}, status = 201)

        except KeyError :
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)
        except UserWallet.DoesNotExist :
            return JsonResponse({"message" : "NO_CASH"}, status = 400)