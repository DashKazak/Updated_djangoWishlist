from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
#created django user model

# Created your placemodels here.

class Place(models.Model):
    user = models.ForeignKey('auth.User', null = False, on_delete = models.CASCADE) 
    #if user is deleted all the info pertained to the user, inlcuded the Places are deleted

    #common types of data fields
    name = models.CharField(max_length=200)
    visited=models.BooleanField(default =False )
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to = 'user_images/',blank=True, null=True)

    def saved(self, *args, **kwargs):
        #saving the new photo instead of an old photo
        old_place = Place.objects.filter(pk = self.pk).first()
        if old_place and old_place.photo:
            if old_place.photo != self.photo:
                self.delete_photo(old_place.photo)
        super().save(*args, **kwargs)
    
    def delete_photo(self, photo):
        if default_storage.exists(photo.name):
            default_storage.delete(photo.name)
        
    def delete(self, *args, **kwargs):
        if self.photo:
            self.delete_photo(self.photo)
        super().delete(args, kwargs)


    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        return f'{self.name} visited? {self.visited}v on {self. date_visited}. Photo {photo_str}'
