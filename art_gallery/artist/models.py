from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Artist(AbstractUser):
    email = models.EmailField(unique=True)
    full_names = models.CharField(max_length=255)
    username = None  # We'll use email as the username

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_names']

    def __str__(self):
        return self.full_names

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.category_name

class Artwork(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='artworks')
    owner = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='artworks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class ArtworkImage(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(image_url__startswith='http'),
                name='valid_image_url'
            )
        ]

    def __str__(self):
        return f"Image for {self.artwork.title}" 