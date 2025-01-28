from django.urls import path
from accounts.views import (
    OshpazRegisterApiView, OshpazLoginApiView, OshpazProfileApiView, OshpazProfileDetailApiView,
    UserRegisterApiView, UserLoginApiView, UserProfileApiView, UserProfileDetailApiView,
    LogoutApiView,
)

urlpatterns = [
    path('oshpaz/register/', OshpazRegisterApiView.as_view()),
    path('oshpaz/login/', OshpazLoginApiView.as_view()),
    path('oshpaz/profile/', OshpazProfileApiView.as_view()),
    path('oshpaz/profile/<int:id>/', OshpazProfileDetailApiView.as_view()),
    path('user/register/', UserRegisterApiView.as_view()),
    path('user/login/', UserLoginApiView.as_view()),
    path('user/profile/', UserProfileApiView.as_view()),
    path('user/profile/<int:id>/', UserProfileDetailApiView.as_view()),
    path('logout/', LogoutApiView.as_view()),
]