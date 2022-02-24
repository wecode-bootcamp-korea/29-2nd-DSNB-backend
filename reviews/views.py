import json

from django.http import JsonResponse

from django.views import View
from reviews.models import Review

class BookReviewView(View):
    def make_review_list(self, objects):
        review_list = [
            {
                "user"
            }
        ]
        return 
    def get(self, request, book_id):
        
        book_reviews = Review.objects.filter(book_id = book_id)\
                        .select_related('writer')\
                        .order_by('-created_at').all()
        
        return JsonResponse({}, status = 200)

# class Review(Base):
#     user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='writer')
#     book       = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='review_book')
#     comment    = models.CharField(max_length=600)
#     rating     = models.DecimalField(max_digits = 3, decimal_places = 2)
#     is_spoiler = models.BooleanField(default = False)
    
#     class Meta:
#         db_table = 'reviews'