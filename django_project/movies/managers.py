import django.db.models as models
from django.db.models import Q


class MovieQuerySet(models.QuerySet):

    def contains(self, name):
        return self.filter(Q(title__contains=name)
                                  | Q(director__contains=name) | Q(genre__contains=name)
                                  | Q(release_date__contains=name))