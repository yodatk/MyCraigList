from django.db import models

MAX_SEARCH_LENGTH = 500


# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=MAX_SEARCH_LENGTH)
    created = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, search):
        output = cls(search=search)
        Search.save(output)
        return output

    def __str__(self):
        return '{}'.format(self.search)

    class Meta:
        verbose_name_plural = 'Searches'
