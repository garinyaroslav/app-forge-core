from django.db import models
from django.contrib.auth.models import AbstractUser


class Consumer(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="consumer_groups",
        related_query_name="consumer",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="consumer_user_permissions",
        related_query_name="consumer",
    )


class Cart(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)


class Review(models.Model):
    text_comment = models.TextField()
    product = models.ForeignKey('SoftwareProduct', on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)


class Library(models.Model):
    product = models.ForeignKey('SoftwareProduct', on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    added_date = models.DateTimeField()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('SoftwareProduct', on_delete=models.CASCADE)


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class SoftwareProduct(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    developer_name = models.CharField(max_length=255)
    rel_date = models.DateTimeField()
    image = models.BinaryField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    copies_sold = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    genres = models.ManyToManyField(Genre, related_name='products')

    def __str__(self):
        return self.title
