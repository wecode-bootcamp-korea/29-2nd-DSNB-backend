import jwt
import datetime
import requests

from django.views import View
from django.http  import JsonResponse
from django.conf  import settings

from users.models import User

class KakaoLoginView(View):
    def get(self, request):
        try:
            kakao_token        = request.headers.get('Authorization')
            user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers = {'Authorization': f'Bearer {kakao_token}'}, timeout = 2)
            user_info          = user_info_response.json()
            kakao_id           = user_info['id']
            nickname           = user_info['kakao_account']['profile']['nickname']
            email              = user_info['kakao_account']['email']
            profile_image_url  = user_info['kakao_account']['profile']['profile_image_url']

            user, created = User.objects.get_or_create(
                kakao_id = kakao_id,
                email    = email,
                defaults = {
                    'nickname'          : nickname,
                    'profile_image_url' : profile_image_url
                }
            )

            result = {
                'name'    : nickname,
                'email'   : email,
                'profile' : profile_image_url
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