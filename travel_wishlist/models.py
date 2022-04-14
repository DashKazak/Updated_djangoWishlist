from unittest.util import _MAX_LENGTH
from django.db import models

# Create your placemodels here.

class Place(models.Model):
    name = models.CharField(max_length=200)
    visited=models.BooleanField(default =False )

    def __str__(self) -> str:
        return f'{self.name} visited? {self.visited}'
