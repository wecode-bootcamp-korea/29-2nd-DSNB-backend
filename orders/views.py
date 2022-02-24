import json

from django.http   import JsonResponse
from django.views  import View

from books.models  import BookOption
from orders.models import Order
from users.models  import UserWallet

from users.utils   import login_required

class BeforeBuyView(View):
    @login_required
    def get(self, request):
        user    = request.user
        wallets = UserWallet.objects.filter(user_id = user)
        result = [{
            'cash' : wallet.cash
        }for wallet in wallets]
        
        return JsonResponse({'message' : 'SUCCESS' , 'result' : result}, status = 200)

class BuyBookView(View):
    @login_required
    def post(self, request):
        data = json.loads(request.body)

        BookOption.objects.create(
            price   = data['price'],
            book_id = data['book_id']
        )

        Order.objects.create(
            user_id         = request.user,
            target_user_id  = request.user,
            order_status_id = 1,
            payment_id      = 1,
            bookoption_id   = data['book_option'],
        )

        return JsonResponse({'message' : 'SUCCESS'}, status = 201)