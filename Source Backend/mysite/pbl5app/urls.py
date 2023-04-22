from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, LoginView, UserList, AdminList, UserUpdateAPIView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('user-list/', UserList.as_view(), name='user-list'),
    path('admin-list/', AdminList.as_view(), name='admin-list'),
    path('users/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user-update'),
]