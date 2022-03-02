from django.urls import re_path, include, path

from .views import RegistrationAPIView, LoginAPIView, ListUserAPIView, ProductAPIView, ProductListAPIView, ProductsGetTopsAPIView, PasswordRecoveryAPIView

urlpatterns = [
    re_path(r'^registration/?$', RegistrationAPIView.as_view(), name='user_registration'),
    re_path(r'^login/?$', LoginAPIView.as_view(), name='user_login'),
    re_path(r'^users/?$', ListUserAPIView.as_view(), name='users_get'),
    re_path(r'^products/?$', ProductAPIView.as_view(), name='products'),
    path('products/<int:id>/', ProductAPIView.as_view(), name='products_get'),
    re_path(r'^recommendation/?$', ProductListAPIView.as_view(), name='products_list'),
    re_path(r'^tops/?$', ProductsGetTopsAPIView.as_view(), name='tops'),
    re_path(r'^recovery/?$', PasswordRecoveryAPIView.as_view(), name='password_recovery'),

]