"""
Models for Product, Variation and Image.
"""
from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.utils.text import slugify


class ProductQuerySet(models.query.QuerySet):
    """
    Query Set for the Product.
    """
    def active(self):
        """
        Active method to filter the query for active products.
        """
        return self.filter(active=True)


class ProductManager(models.Manager):
    """
    Model Manager for Product.
    """
    def get_queryset(self):
        """
        Default query set.
        """
        return ProductQuerySet(self.model, using=self._db)

    def all(self, *args, **kwargs):
        """
        Modify the all() method to return only active products.
        """
        return self.get_queryset().active()

    def get_related(self, instance):
        """
        Method to return related products.
        Retrieves the instance as a parameter and filters the products
        that has the same category and default category.
        Excludes the instance itself, as well as the duplicates.
        Returns the filtered products.
        """
        products_one = self.get_queryset().filter(categories__in=instance.categories.all())
        products_two = self.get_queryset().filter(default=instance.default)
        queryset = (products_one | products_two).exclude(id=instance.id).distinct()
        return queryset



class Product(models.Model):
    """
    Product model.
    """
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default=True)
    categories = models.ManyToManyField("Category", blank=True)
    default = models.ForeignKey("Category", related_name='default_category', null=True, blank=True, on_delete=models.CASCADE)

    objects = ProductManager()

    class Meta:
        """
        Ordered by title.
        """
        ordering = ["-title"]

    def __str__(self):
        """
        Return human readable representation of the model.
        """
        return self.title

    def get_absolute_url(self):
        """
        Method to tell Django how to calculate the canonical URL for an object.
        """
        return reverse('product_detail', kwargs={'pk': self.pk})

    def get_image_url(self):
        """
        Returns the image for a product. if a product does not have an image,
        then it returns None.
        """
        img = self.productimage_set.first()
        if img:
            return img.image.url
        return img


class Variation(models.Model):
    """
    Variation model.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    active = models.BooleanField(default=True)
    inventory = models.IntegerField(null=True, blank=True) # -1 or none refers to unlimited
    sale_price = models.DecimalField(decimal_places=2, max_digits=20, null=True, blank=True)

    def __str__(self):
        """
        Return human readable representation of the model.
        """
        return self.title

    def get_price(self):
        """
        if sale price exist return the sale price.
        Otherwise return the regular price.
        """
        if self.sale_price is not None:
            return self.sale_price
        return self.price

    def get_absolute_url(self):
        """
        Method to tell Django how to calculate the canonical URL for an object.
        """
        return self.product.get_absolute_url()

def product_post_saved_receiver(sender, instance, created, *args, **kwargs):
    """
    Create a default Variation for products that do not have a variation.
    """
    product = instance
    variations = product.variation_set.all()
    if variations.count() == 0:
        new_var = Variation()
        new_var.product = product
        new_var.title = 'Default'
        new_var.price = product.price
        new_var.save()

post_save.connect(product_post_saved_receiver, sender=Product)


class Category(models.Model):
    """
    Models for the Category.
    """
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug })


def image_upload_to(instance, filename):
    """
    Upload image to particular location.
    """
    title = instance.product.title
    slug = slugify(title)
    basename, file_extension = filename.split('.')
    new_filename = "{}{}.{}".format(basename, instance.id, file_extension)
    return "products/{}/{}".format(slug, new_filename)


class ProductImage(models.Model):
    """
    Image class for products. One to Many relationship.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=image_upload_to)

    def __str__(self):
        """
        Return human readable representation of the model.
        """
        return self.product.title
