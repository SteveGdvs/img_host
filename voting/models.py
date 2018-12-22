from django.db import models
from django.conf import settings

from images.models import Image


class Vote(models.Model): # to theloume gia bookkeeping poios exei kanei like
	image = models.ForeignKey(Image, on_delete=models.CASCADE)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	vote = models.NullBooleanField(default=None, blank=True, null=True)

	NOTHING = None
	LIKE = True
	DISLIKE = False

	def __str__(self):
		if self.vote is True:
			vote_str = 'Liked'
		elif self.vote is False:
			vote_str = 'Disliked'
		else:
			vote_str = 'Nothing'
		string = '{0} {1} {2}'.format(self.user, vote_str, self.image)
		return string
