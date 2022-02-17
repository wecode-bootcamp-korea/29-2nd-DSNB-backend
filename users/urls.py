from django.urls import path

from .views import KakaoLoginView

urlpatterns = [
    path('/kakao-auth' , KakaoLoginView.as_view()),
]