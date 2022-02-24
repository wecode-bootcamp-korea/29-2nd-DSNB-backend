from django.urls import path
from orders.views import BeforeBuyView, BuyBookView

urlpatterns = [
    path('/info',BeforeBuyView.as_view()),
    path('/buy',BuyBookView.as_view())
]