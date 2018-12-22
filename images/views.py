from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404, redirect, render

from .models import Image
from .forms import ImageForm
from voting.models import Vote


def home(request):
	images = Image.objects.all().order_by("-uploaded")[:10]

	score_dict = {}
	votes_dict = {}

	for image in images:
		score_dict[image.id] = image.score

	if request.user.is_authenticated:
		votes = Vote.objects.filter(image__in=images, user=request.user)
		for vote in votes:
			votes_dict[vote.image.id] = vote

	context = {'images': images, 'votes_dict': votes_dict, 'score_dict': score_dict}

	return render(request, 'images/image_list.html', context)


def view_image(request, image_id):
	image = Image.objects.get(id=image_id)

	if request.user.is_authenticated:
		try:
			user_vote = Vote.objects.get(user=request.user, image=image)  # only the vote from the current user
		except Vote.DoesNotExist:
			user_vote = None
	else:
		user_vote = None

	context = {'image': image, 'user_vote': user_vote}

	return render(request, 'images/image.html', context)


def popular_images(request):
	images = Image.objects.all().order_by("-score")

	score_dict = {}
	votes_dict = {}

	for image in images:
		score_dict[image.id] = image.score

	if request.user.is_authenticated:
		votes = Vote.objects.filter(image__in=images, user=request.user)
		for vote in votes:
			votes_dict[vote.image.id] = vote

	context = {'images': images, 'votes_dict': votes_dict, 'score_dict': score_dict}

	return render(request, 'images/image_list.html', context)


def latest_images(request):
	period = request.GET.get('p', 'week')

	if period == 'day':
		period = datetime.now() - timedelta(days=1)
	if period == 'week':
		period = datetime.now() - timedelta(days=7)
	if period == 'month':
		period = datetime.now() - timedelta(days=30)

	images = Image.objects.all().order_by("-uploaded").filter(uploaded__gt=period)

	score_dict = {}
	votes_dict = {}

	for image in images:
		score_dict[image.id] = image.score

	if request.user.is_authenticated:
		votes = Vote.objects.filter(image__in=images, user=request.user)
		for vote in votes:
			votes_dict[vote.image.id] = vote

	context = {'images': images, 'votes_dict': votes_dict, 'score_dict': score_dict}

	return render(request, 'images/image_list.html', context)


def upload_image(request):
	if request.method == 'POST':
		image_form = ImageForm(request.POST, request.FILES)
		if image_form.is_valid():
			image = image_form.save(commit=False)
			image.user = request.user
			image.save()
			return redirect('images:image', image_id=image.id)
	else:
		image_form = ImageForm()
	context = {'image_form': image_form}
	return render(request, "images/upload_image.html", context)


def my_uploads(request):
	images = Image.objects.all().filter(user=request.user)
	context = {'images': images}
	return render(request, "images/my_uploads.html", context)


def delete_image(request, image_id):
	image = get_object_or_404(Image, id=image_id)

	image.delete()
	return redirect('images:my_uploads')


def edit_image(request, image_id):
	image = get_object_or_404(Image, id=image_id)

	if request.method == 'POST':
		image_form = ImageForm(request.POST, request.FILES, instance=image)
		if image_form.is_valid():
			image_form.save()
			return redirect('images:image', image_id=image.id)
	else:
		image_form = ImageForm(instance=image)
	context = {'image': image, 'image_form': image_form}
	return render(request, "images/image_edit.html", context)


def search_image(request):
	query = request.GET.get('s', None)

	if query is None:
		images = None
	else:
		images = Image.objects.all().filter(title__startswith=query)

	score_dict = {}
	votes_dict = {}

	for image in images:
		score_dict[image.id] = image.score

	if request.user.is_authenticated:
		votes = Vote.objects.filter(image__in=images, user=request.user)
		for vote in votes:
			votes_dict[vote.image.id] = vote

	context = {'images': images, 'votes_dict': votes_dict, 'score_dict': score_dict}

	return render(request, 'images/image_list.html', context)
