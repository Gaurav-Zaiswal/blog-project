import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    # customizing fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    email = models.EmailField(verbose_name='email', max_length=256, unique=True)

    USERNAME_FIELD = 'email'  # now user can log in using email
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name'] # here, email is already a required field

    def __str__(self):
        return self.username


def profile_pic_path(instance, filename):
    # checks jpg exttension
    extention = filename.split('.')[1]
    if len(filename.split('.')) != 2:
        raise ValidationError("image seems currupted...")
    if not extention in ['jpg', 'jpeg']:
        raise ValidationError("we currently accept jpg/jpeg formats only.")
    unique_name = uuid.uuid4().hex
    print('thumbnail_path/' + unique_name + '.' + extension)

    return 'thumbnail_path/' + unique_name + '.' + extension


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(default='default_pic_author.jpg',
                              upload_to = profile_pic_path)

    def __str__(self):
        return f'{self.user.username} Profile'
