from django.urls import path

from . import views


app_name = 'images'

urlpatterns = [
	path('', views.home, name='home'),
	path('image/upload', views.upload_image, name='image_upload'),
	path('image/<int:image_id>', views.view_image, name='image'),
	path('image/search/', views.search_image, name='image_search'),
	path('popular', views.popular_images, name='images_popular'),
	path('latest', views.latest_images, name='image_latest'),
	path('my_uploads', views.my_uploads, name='my_uploads'),
	path('image/delete/<int:image_id>', views.delete_image, name='image_delete'),
	path('image/edit/<int:image_id>', views.edit_image, name='image_edit')
]
