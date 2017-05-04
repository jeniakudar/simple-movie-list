from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import MovieQuerySet


class Movie(models.Model):
    GENRE_OPTIONS = (
        ('Horror', 'Horror'),
        ('Drama', 'Drama'),
        ('Comedy', 'Comedy'),
        ('Action', 'Action'),
        ('Crime', 'Crime')
    )
    title = models.CharField(max_length=50)
    release_date = models.IntegerField(blank=True, null=True)
    director = models.CharField(max_length=30, blank=True)
    duration = models.IntegerField(blank=True, null=True)
    genre = models.CharField(max_length=10, choices=GENRE_OPTIONS)
    description = models.TextField(max_length=1000, blank=True)

    objects = MovieQuerySet.as_manager()

    def __str__(self):
        return "%s" % (self.title)


class Photo(models.Model):

    file = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'


class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Driver.objects.create(user=instance)
    instance.driver.save()

