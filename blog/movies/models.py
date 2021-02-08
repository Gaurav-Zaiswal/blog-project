import datetime
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model  # another way to import User
from django.utils import timezone
from django.urls import reverse
from django.template.defaultfilters import slugify

from users.models import Profile

# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

STATUS = (
    (0, "Draft"),
    (1, "Publish")
)

# When time zone support is enabled (USE_TZ=True), Django uses time-zone-aware datetime objects.
# If your code creates datetime objects, they should be aware too
# same as datetime.datetime.now()
now = timezone.now()
today = datetime.datetime.now()


def thumbnail_path(instance, filename):
    # checks jpg exttension
    extension = filename.split('.')[1]
    if len(filename.split('.')) != 2:
        raise TypeError("image seems currupted...")
    if extension not in ['jpg', 'jpeg', 'JPG', 'JPEG']:
        raise TypeError("we currently accept jpg/jpeg formats only.")
    unique_name = uuid.uuid4().hex
    new_file_name = 'poster/' + today.strftime("%Y") + '/' + \
                    today.strftime("%m") + '/' + unique_name + '.' + extension

    return new_file_name


# ======================== #
#     MODELS HERE         #
# ======================= #


class Movie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=70, null=True, blank=True)
    poster = models.ImageField(upload_to=thumbnail_path, max_length=52, null=True, blank=True)
    updated_on = models.DateTimeField('Date and Time', auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField('Status', choices=STATUS, default=0)
    # content = models.TextField()

    # implementing ckeditor app's richtextfield on content
    review = RichTextUploadingField()

    # validating created_on, so that user cannot select past date
    # also known as field level validation
    def clean_created_on(self):
        """Make sure expiry time cannot be in the past"""

        if self.created_on and self.created_on < now:
            raise ValidationError('Please, pick present date and time...')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Movie, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        post_created_day = self.created_on.day
        if post_created_day in range(0, 10):
            post_created_day = "0" + str(post_created_day)  # 9 will be 09, as url req 2 digits

        return reverse('posts:detail-post',
                       kwargs={
                           'year': str(self.created_on.year),
                           'month': str(self.created_on.month),
                           'day': post_created_day if type(post_created_day) == str else str(post_created_day),
                           'slug': self.slug,
                       }
                       )


class MovieRating(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE, primary_key=True)
    updated_on = models.DateTimeField('Date and Time', auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField('Status', choices=STATUS, default=0)

    plot = models.models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0)
    theme = models.models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0)
    acting = models.models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0)
    direction = models.models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0)
    bg_music = models.models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0)
    cinematography = models.models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0)
    production_design = models.models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0)
    pace = models.models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0)
    editing = models.models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0)
    dialogue = models.models.DecimalField(
        max_digits=2,
        decimal_places=1,
        default=0)

    # validating created_on, so that user cannot select past date
    # also known as field level validation
    def clean_created_on(self):
        """Make sure expiry time cannot be in the past"""

        if self.created_on and self.created_on < now:
            raise ValidationError('Please, pick present date and time...')
    #validate all ratings so that they lies in 1 to 10

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

