from django.urls import path

from .views import KakaoLoginView, UserLibraryView, LibrarySearchView

urlpatterns = [
    path('/kakao-auth' , KakaoLoginView.as_view()),
    path('/library', UserLibraryView.as_view()),
    path('', LibrarySearchView.as_view())
]