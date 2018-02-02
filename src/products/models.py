from django.db import models


class Product(models.Model):
    title           = models.CharField(max_length=120)
    description     = models.TextField(blank=True, null=True)
    price           = models.DecimalField(decimal_places=2, max_digits=20)
    active          = models.BooleanField(default=True)
    categories      = models.ManyToManyField('Category', blank=True)
    default         = models.ForeignKey('Category', related_name='default_category', null=True, blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
