from django.db import models

MAX_SEARCH_LENGTH = 500


# Create your models here.
class Search(models.Model):
    search_field = models.CharField(max_length=MAX_SEARCH_LENGTH)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}'.format(self.search_field)

    class Meta:
        verbose_name_plural = 'Searches'
