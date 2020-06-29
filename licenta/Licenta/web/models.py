from django.contrib.auth.models import Permission, User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from PIL import Image

class Movie(models.Model):
	title   	= models.CharField(max_length=200)
	genre  		= models.CharField(max_length=100)
	movie_logo  = models.FileField()

	class Meta:
		ordering = ('title', 'genre')

		def __str__(self):
			return '{} ({})'.format(self.title, self.genre)


		def __str__(self):
			return self.title 

class Myrating(models.Model):
	user   	= models.ForeignKey(User,on_delete=models.CASCADE) 
	movie 	= models.ForeignKey(Movie,on_delete=models.CASCADE)
	rating 	= models.IntegerField(default=1,validators=[MaxValueValidator(5),MinValueValidator(0)])
		

class Profile1(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self):
		super().save()

		img = Image.open(self.image.path)

		if img.height > 300 or img.width > 300:
			output_size = (300, 300)
			img.thumbnail(output_size)
			img.save(self.image.path)


   