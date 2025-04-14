from django.urls import path
from .views import login_view, whoami_view, signUp, logout_view
from . import views

urlpatterns = [
    path('login/', login_view, name='login'),
    path('whoami/', whoami_view, name='whoami'),
    path('signUp/', signUp, name='signUp'),
    path('favorites/', views.get_user_favorites, name='get_favorites'),
    path('favorites/add/<int:anime_id>/', views.add_to_favorites, name='add_favorite'),
    path('favorites/remove/<int:anime_id>/', views.remove_from_favorites, name='remove_favorite'),
    path('logout/', logout_view, name='logout'),
]
