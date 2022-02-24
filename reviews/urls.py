from django.urls import path

from reviews.views import BookReviewView

urlpatterns = [
    path('/<int:book_id>',BookReviewView.as_view()),
]