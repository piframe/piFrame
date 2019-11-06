from django.db import models
from .fitimage import fit
from django.conf import settings

# Create your models here.


class Artwork(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='originals')
    _portrait = models.CharField(max_length=100, null=True, db_column="portrait")
    _landscape = models.CharField(max_length=100, null=True, db_column="landscape")

    # hacky af
    @property
    def landscape(self):
        x = self._landscape
        x = x.split("media")
        x = "/media" + x[-1]
        return x

    @landscape.setter
    def landscape(self, value):
        self._landscape = value

    # hacky af
    @property
    def portrait(self):
        x = self._portrait
        x = x.split("media")
        x = "/media" + x[-1]
        return x

    @portrait.setter
    def portrait(self, value):
        self._portrait = value

    def save(self, *args, **kwargs):
        img = fit(self.photo.file, settings.FRAME_RESOLUTION, settings.MEDIA_ROOT)
        self._landscape, self.portrait = img
        super(Artwork, self).save(*args, **kwargs)  # Call the "real" save() method.

    class Meta:
        ordering = ['-created_date']
