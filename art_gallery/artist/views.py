from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import Artist, Category, Artwork, ArtworkImage
from .serializers import (
    ArtistSerializer, CategorySerializer, ArtworkSerializer,
    ArtworkListSerializer, ArtworkImageSerializer
)

# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = ArtistSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = Artist.objects.filter(email=email).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

class ArtworkListView(generics.ListCreateAPIView):
    queryset = Artwork.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ArtworkSerializer
        return ArtworkListSerializer

    def get_queryset(self):
        category_name = self.request.query_params.get('category')
        if category_name:
            return Artwork.objects.filter(category__category_name=category_name)
        return Artwork.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ArtworkDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Artwork.objects.all()
    serializer_class = ArtworkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'GET':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_object(self):
        obj = get_object_or_404(Artwork, id=self.kwargs['artwork_id'])
        if self.request.method in ['PUT', 'DELETE']:
            if obj.owner != self.request.user:
                self.permission_denied(self.request)
        return obj

class ArtistArtworkListView(generics.ListAPIView):
    serializer_class = ArtworkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Artwork.objects.filter(owner=self.request.user)

class CategoryArtworkListView(generics.ListAPIView):
    serializer_class = ArtworkListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return Artwork.objects.filter(category_id=category_id)

class UserArtworkListView(generics.ListAPIView):
    serializer_class = ArtworkListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        # Only allow users to view their own artworks
        if self.request.user.id != user_id:
            self.permission_denied(self.request)
        return Artwork.objects.filter(owner_id=user_id)
