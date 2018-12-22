from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

from images.models import Image
from .models import Vote


@login_required
def vote_like(request):
	if request.is_ajax():
		data = {}
		image_id = request.POST.get('image_id')
		image = get_object_or_404(Image, id=image_id)
		vote, created = Vote.objects.get_or_create(image=image, user=request.user)

		if vote.vote is Vote.LIKE:
			image.score -= 1
			vote.vote = Vote.NOTHING
			data['action'] = 'remove'
		elif vote.vote is Vote.NOTHING:
			image.score += 1
			vote.vote = Vote.LIKE
			data['action'] = 'add'
		elif vote.vote is Vote.DISLIKE:
			image.score += 2
			vote.vote = Vote.LIKE
			data['action'] = 'add'

		image.save()
		vote.save()
		data['score'] = image.score
		return JsonResponse(data=data, status=200)
	else:
		return HttpResponse(status=405)  # 405 Method Not Allowed


@login_required
def vote_dislike(request):
	if request.is_ajax():
		data = {}
		image_id = request.POST.get('image_id')
		image = get_object_or_404(Image, id=image_id)
		vote, created = Vote.objects.get_or_create(image=image, user=request.user)
		if vote.vote is Vote.DISLIKE:
			image.score += 1
			vote.vote = Vote.NOTHING
			data['action'] = 'remove'
		elif vote.vote is Vote.NOTHING:
			image.score -= 1
			vote.vote = Vote.DISLIKE
			data['action'] = 'add'
		elif vote.vote is Vote.LIKE:
			image.score -= 2
			vote.vote = Vote.DISLIKE
			data['action'] = 'add'

		image.save()
		vote.save()
		data['score'] = image.score
		return JsonResponse(data=data, status=200)
	else:
		return HttpResponse(status=405)  # 405 Method Not Allowed
