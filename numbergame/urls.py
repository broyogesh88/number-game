from django.contrib import admin
from django.urls import path, include
from game import views  # ✅ Add this line

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.create_game, name='home'),  # ✅ Redirect root URL to game create
    path('', include('game.urls')),            # Your existing game URLs
]
