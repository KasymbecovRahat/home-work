from django.urls import path
from .views import *

urlpatterns = [

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', ProductListViewSet.as_view({'get': 'list', 'post': 'create'}), name='product_list'),
    path('<int:pk>/', ProductViewSet.as_view({'get': 'retrieve',
                                              'delete': 'destroy',
                                              'put': 'update'}), name='product_detail'),

    path('user', UserProfileViewSet.as_view({'get': 'list', 'post': 'create'}), name='user_list'),
    path('user/<int:pk>/', UserProfileViewSet.as_view({'get': 'retrieve',
                                                       'delete': 'destroy',
                                                       'put': 'update'}), name='user_detail'),

    path('category', CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category_list'),
    path('category/<int:pk>/', CategoryViewSet.as_view({'get': 'retrieve',
                                                        'delete': 'destroy',
                                                        'put': 'update'}), name='category_detail'),

    path('photo', ProductPhotoViewSet.as_view({'get': 'list', 'post': 'create'}), name='photo_list'),
    path('photo/<int:pk>/', ProductPhotoViewSet.as_view({'get': 'retrieve',
                                                         'delete': 'destroy',
                                                         'put': 'update'}), name='photo_detail'),

    path('raitings', RaitingsViewSet.as_view({'get': 'list', 'post': 'create'}), name='raiting_list'),
    path('raitings/<int:pk>/', RaitingsViewSet.as_view({'get': 'retrieve',
                                                      'delete': 'destroy',
                                                      'put': 'update'}), name='raiting_detail'),

    path('review', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='review_list'),
    path('review/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve',
                                                    'delete': 'destroy',
                                                    'put': 'update'}), name='review_detail'),


    path('cart/',CartViewSet.as_view({'get':'retrieve'}),name='cart_detail'),

    path('cart_items/',CartItemViewSet.as_view({'get': 'list', 'post': 'create'}),name='cart_items'),
    path('cart_items/int/pk/',CartItemViewSet.as_view({
                                                   'delete': 'destroy',
                                                   'put': 'update'}), name='cart_items'),

]