from django.db import models
from .fitimage import fit
from django.conf import settings

# Create your models here.


class Artwork(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='originals')
    landscape = models.CharField(max_length=100, null=True)
    portrait = models.CharField(max_length=100, null=True)

    def save(self, *args, **kwargs):
        img = fit(self.photo.file, settings.FRAME_RESOLUTION, self.photo.path)
        self.landscape, self.portrait = img
        super(Artwork, self).save(*args, **kwargs)  # Call the "real" save() method.

    class Meta:
        ordering = ['-created_date']
