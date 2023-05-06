from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, LoginView, UserList, AdminList, UserUpdateAPIView, UserPasswordUpdateAPIView, receive_encode_face, receive_image

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('user-list/', UserList.as_view(), name='user-list'),
    path('admin-list/', AdminList.as_view(), name='admin-list'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
    path('users/<int:pk>/password-change/', UserPasswordUpdateAPIView.as_view(), name='user-change-password'),
    path('receive_encode_face/', receive_encode_face, name='receive_encode_face'),
    path('receive_image/', receive_image, name='receive_imgae'),
    

]