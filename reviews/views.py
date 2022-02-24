import json

from django.http import JsonResponse

from django.views import View
from reviews.models import Review

class BookReviewView(View):

    def make_review_list(self, reviews, user_id):
        review_list = [
            {
                "user_id"    : review.user.id,
                "nickname"   : review.user.nickname,
                "comment"    : review.comment,
                "rating"     : review.rating,
                "is_spoiler" : review.is_spoiler,
                "created_at" : review.created_at,
                "is_edit"    : 'y' if user_id == review.user.id else 'n'
            }for review in reviews
        ]
        return review_list

    def get(self, request, book_id):
        try :
            user_id = 3
            book_reviews = Review.objects.filter(book_id = book_id)\
                            .select_related('user')\
                            .order_by('-created_at').all()
        
            result_data   = dict()
            result_data['reviews'] = self.make_review_list(book_reviews, user_id)
            result_data['result']  = 'success'

            return JsonResponse(result_data, status = 200)
        except Review.DoesNotExist:
            return JsonResponse({"message" : "no_asset"}, status = 404)