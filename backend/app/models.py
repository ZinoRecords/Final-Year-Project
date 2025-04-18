from django.db import models
from django.contrib.auth.models import AbstractUser

class AnimeUser(AbstractUser):
    # Add your custom fields here
    role = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Anime(models.Model):
    # Table 'Anime'
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    description = models.TextField()
    imageURL = models.URLField(verbose_name='URL to the anime image')
    releaseDate = models.DateField()
    genre = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    characters = models.TextField()

    def __str__(self):
        return self.name


class FavJunction(models.Model):
    # Table 'FavJunction'
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AnimeUser, on_delete=models.CASCADE, related_name='favorites')
    anime = models.ForeignKey(Anime, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'anime')  # Ensures no duplicate user-anime relationships

    def __str__(self):
        return f"{self.user.username} - {self.anime.name}"
