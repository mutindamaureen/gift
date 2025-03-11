from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)

    def get_absolute_url(self):
        return f'/{self.slug}/'

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', null=True, blank=True)
    thumbnail = models.ImageField(upload_to='uploads/thumbnails/', null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-date_added',)

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):  # Use a tuple instead of a set
        img = Image.open(image)

        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
        
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=85)  # Use format='JPEG'

        # Create a ContentFile from the BytesIO object
        thumbnail = ContentFile(thumb_io.getvalue(), name=self.image.name)  # Use ContentFile

        return thumbnail

    def save(self, *args, **kwargs):
        if self.image:
            self.thumbnail = self.make_thumbnail(self.image)
        super().save(*args, **kwargs)