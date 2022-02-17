from django.urls import path
from books.views import BookListView, BookDetailView , NavCategoryView
urlpatterns = [
    path('',BookListView.as_view()), # 전체 책들 조회 +필터링
    path('/nav', NavCategoryView.as_view()),
    path('/<int:category_id>',BookListView.as_view()), # 특정 국가의 책들 조회 + 필터링
    path('/book/<int:book_id>',BookDetailView.as_view()) #책 상세 페이지
]