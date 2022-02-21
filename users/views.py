import jwt
import datetime
import requests
import json

from django.views     import View
from django.http      import JsonResponse
from django.conf      import settings
from django.db.models import Q

from users.models     import UserLibrary
from books.models     import Book
from users.models     import User
from users.utils      import login_required

class KakaoLoginView(View):
    def get(self, request):
        try:
            kakao_token        = request.headers.get('Authorization')
            user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers = {'Authorization': f'Bearer {kakao_token}'}, timeout = 2)
            user_info          = user_info_response.json()
            kakao_id           = user_info['id']
            nickname           = user_info['kakao_account']['profile']['nickname']
            email              = user_info['kakao_account']['email']
            profile_image      = user_info['kakao_account']['profile']['profile_image_url']

            user, created = User.objects.get_or_create(
                kakao_id = kakao_id,
                email    = email,
                defaults = {
                    'nickname'          : nickname,
                    'profile_image' : profile_image
                }
            )

            result = {
                'name'              : nickname,
                'email'             : email,
                'profile_image_url' : profile_image
            }

            access_token = jwt.encode({'user_id' : user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)}, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse(
                {
                    'message'   : 'SUCCESS',
                    'token'     : access_token,
                    'user_info' : result
                }, status = 200)
            
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message' : 'EXPIRED_TOKEN'}, status = 400)            

class UserLibraryView(View):
    @login_required
    def get(self, request):
        user = request.user
        books = UserLibrary.objects.filter(user = user)
        result = [{
            'title'       : book.book.title,
            'author'      : book.book.author.name,
            'bookmark'    : book.bookmark,
            'rating'      : book.book.everage_rate,
            'file_url'    : book.book.file_url,
            'cover_image' : book.book.cover_image
        }for book in books]

        return JsonResponse({'message' : result}, status = 200)

    @login_required
    def patch(self, request):
        try:
            user = request.user
            data = json.loads(request.body)
            UserLibrary.objects.filter(book = data['book_id'], user = user)\
                .update(bookmark = data['bookmark'])

            return JsonResponse({'message' : 'SUCCESS'}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

class LibrarySearchView(View):
    def get(self, request):
        try:
            search = request.GET.get('search')
            books  = Book.objects.filter(Q(title__icontains = search) | Q(author__name__icontains = search))

            result = [{
                'title'  : book.title,
                'author' : book.author.name
            }for book in books]

            return JsonResponse({'message' : 'SUCCESS', 'result' : result})

        except Book.DoesNotExist:
            return JsonResponse({'message' : 'NO_BOOK'}, status = 400)