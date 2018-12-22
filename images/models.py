from django.db import models
from django.conf import settings


class Image(models.Model):
	title = models.CharField(max_length=40)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	img_file = models.ImageField()
	uploaded = models.DateTimeField(auto_now_add=True)

	score = models.IntegerField(default=0)

	def __str__(self):
		return self.title