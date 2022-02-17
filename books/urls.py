from django.urls import path
from books.views import BookListView, BookDetailView , NavCategoryView
urlpatterns = [
    path('',BookListView.as_view()),
    path('/nav', NavCategoryView.as_view()),
    path('/<int:category_id>',BookListView.as_view()),
    path('/book/<int:book_id>',BookDetailView.as_view())
]