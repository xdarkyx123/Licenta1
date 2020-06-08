from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)


	def __str__(self):
		return self.title
	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})



class Movie(models.Model):
	title = models.CharField(max_length=200)
	genre = models.CharField(max_length=100)
	movie_logo = models.FileField()

	def __str__(self):
		return self.title



class Myrating(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
	rating = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(0)])

