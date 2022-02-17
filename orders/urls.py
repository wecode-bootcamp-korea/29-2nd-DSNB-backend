from django.urls import path
from orders.views import OrderBookView
urlpatterns = [
    path( '', OrderBookView.as_view()), #get이면...책 주문전 이메일 확인, post면 주문 하기
    path('/delete/<int:order_id>',OrderBookView.as_view()),
]