from django.db import models
from django.urls import reverse


class Service(models.Model):
    name = models.CharField(max_length=255, verbose_name="Атауы")
    content = models.TextField(blank=True, verbose_name="Ақпарат")
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", verbose_name="Сурет")
    price = models.CharField(max_length=255, verbose_name="Бағасы")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Created Time")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Updated time")
    is_published = models.BooleanField(default=True,)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service', kwargs={'service_slug': self.slug})

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Category")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


