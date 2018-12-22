from django.urls import path

from . import views


app_name = 'voting'

urlpatterns = [
	path('vote/like/', views.vote_like, name='vote-like'),
	path('vote/dislike/', views.vote_dislike, name='vote-dislike'),
]