from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    authors = models.CharField(max_length=200, blank=True)
    publication_date = models.CharField(max_length=50, default=None, blank=True)
    google_reviews = models.CharField(max_length=3, default=None, blank=True)


    Books = models.Manager()

    def __str__(self):
        return self.title





