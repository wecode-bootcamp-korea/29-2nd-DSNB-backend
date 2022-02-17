## json response 파일 작성을 위한 OOP type 스크립트 연습용
import json
from django.http import JsonResponse

class BookSorting():
    
    #책을 리뷰순으로 정렬
    def rank_by_review(self, book, **kargs):
        return 1
    #책을 점수순으로 정렬
    def rank_by_updatedorscore(self, book, **kargs):
        return 1
