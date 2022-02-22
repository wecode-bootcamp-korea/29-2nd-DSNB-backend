from django.urls import path
from books.views import BookListView, BookDetailView , NavCategoryView, BestSellerView, LocationView, SlideView, SearchView, BookRankView
urlpatterns = [
    path('/', SearchView.as_view()),
    path('/nav', NavCategoryView.as_view()),
    path('/page', BestSellerView.as_view()),
    path('/rank', BookRankView.as_view()),
    path('/slide' , SlideView.as_view()),
    path('/location', LocationView.as_view()),
    path('/nation',BookListView.as_view()),
    path('/<int:book_id>',BookDetailView.as_view()),
    path('/nation/<int:category_id>',BookListView.as_view())
]