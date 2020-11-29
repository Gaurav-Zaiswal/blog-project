import uuid
import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

from django_countries.fields import CountryField

# Create your models here.


def profile_pic_path(instance, filename):
	# checks jpg exttension
	extension = filename.split('.')[1]
	if len(filename.split('.')) != 2:
		raise ValidationError("image seems currupted...")
	if extension not in ['jpg', 'jpeg']:
		raise ValidationError("we currently accept jpg/jpeg formats only.")
	unique_name = uuid.uuid4().hex
	# print('author_pictures/' + unique_name + '.' + extension)

	return 'author_pictures/' + unique_name + '.' + extension


def validate_age(date):
	if abs(date - datetime.date.today()) < datetime.timedelta(15):
		raise ValidationError("You must be 15 years old")



class User(AbstractUser):
	# customizing fields
	id = models.UUIDField(primary_key=True, default=uuid.uuid4)
	email = models.EmailField(verbose_name='email', max_length=256, unique=True)

	USERNAME_FIELD = 'email'  # now user can log in using email
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']  # here, email is already a required field

	def __str__(self):
		return self.username


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	image = models.ImageField(
		default='default_pic_author.jpg',
		upload_to=profile_pic_path)
	dob = models.DateField(auto_now=False, auto_now_add=False, null=True, validators=[validate_age])
	country = CountryField(blank_label='(select country)', null=True)
	# isEligible = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.user.username} Profile'
