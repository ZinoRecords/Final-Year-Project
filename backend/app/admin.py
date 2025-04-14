from django.contrib import admin
from .models import AnimeUser, Anime, FavJunction

admin.site.register(AnimeUser)
admin.site.register(Anime)
admin.site.register(FavJunction)
