from django.urls import path
from books.views import BookListView
urlpatterns = [
    path('',BookListView.as_view()), # 전체 책들 조회
    path('/<int:category_id>',BookListView.as_view()), # 특정 국가의 책들 조회
    #path('detail/<int:book_id>', ) #책 상세 페이지
]