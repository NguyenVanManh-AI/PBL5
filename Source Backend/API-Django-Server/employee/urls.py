from django.urls import path, re_path
from . import views

from django.urls import path
from .views import FileUploadView

# lấy ảnh ra để xem 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    re_path(
        r'^api/employee/(?P<pk>[0-9]+)$',
        views.get_delete_update_employee,
        name='get_delete_update_employee'
    ),
    path(
        'api/employee/',
        views.get_post_employee,
        name='get_post_employee'
    ),
    # cũ 
    # path(
    #     'api/upload/',
    #     views.upload,
    #     name='upload'
    # ),
    path('api/upload-file', FileUploadView.as_view(), name='upload-file'), # upload files 
    path('api/images', views.get_images, name='images'), # get images of user , views.get_images là hàm get_images trong file views
    path('api/update-images', views.update_images, name='update-images'), # update images 
    path('api/all-images/',views.all_images,name='all-images'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # lấy ảnh ra để xem

# from django.conf.urls import url
# from . import views

# urlpatterns = [
#     url(
#         r'^api/employee/(?P<pk>[0-9]+)$',
#         views.get_delete_update_employee,
#         name='get_delete_update_employee'
#     ),
#     url(
#         r'^api/employee/$',
#         views.get_post_employee,
#         name='get_post_employee'
#     )
# ]
