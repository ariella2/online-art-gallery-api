from django.urls import path
from .views import (
    RegisterView, LoginView, CategoryListView,
    ArtworkListView, ArtworkDetailView, ArtistArtworkListView,
    CategoryArtworkListView, UserArtworkListView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), #working
    path('login/', LoginView.as_view(), name='login'), #working
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('artworks/', ArtworkListView.as_view(), name='artwork-list'),
    path('artworks/artwork/<int:artwork_id>/', ArtworkDetailView.as_view(), name='artwork-detail'),
    path('artworks/category/<int:category_id>/', CategoryArtworkListView.as_view(), name='category-artworks'),
    path('artworks/user/<int:user_id>/', UserArtworkListView.as_view(), name='user-artworks'),
    path('my-artworks/', ArtistArtworkListView.as_view(), name='artist-artworks'),
] 