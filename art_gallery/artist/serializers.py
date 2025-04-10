from rest_framework import serializers
from .models import Artist, Category, Artwork, ArtworkImage

class ArtistSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Artist
        fields = ('id', 'email', 'full_names', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        artist = Artist(**validated_data)
        artist.set_password(password)
        artist.save()
        return artist

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'category_name', 'created_at')

class ArtworkImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkImage
        fields = ('id', 'image_url', 'is_primary')

class ArtworkSerializer(serializers.ModelSerializer):
    images = ArtworkImageSerializer(many=True)
    category_name = serializers.CharField(source='category.category_name', read_only=True)
    owner_name = serializers.CharField(source='owner.full_names', read_only=True)

    class Meta:
        model = Artwork
        fields = ('id', 'title', 'description', 'category', 'category_name', 
                 'owner', 'owner_name', 'images', 'created_at', 'updated_at')
        read_only_fields = ('owner',)

    def validate(self, data):
        images = data.get('images', [])
        if len(images) < 3:
            raise serializers.ValidationError("At least 3 images are required")
        if len(images) > 5:
            raise serializers.ValidationError("Maximum 5 images are allowed")
        
        primary_images = [img for img in images if img.get('is_primary', False)]
        if len(primary_images) != 1:
            raise serializers.ValidationError("Exactly one image must be marked as primary")
        
        return data

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        artwork = Artwork.objects.create(**validated_data)
        
        for image_data in images_data:
            ArtworkImage.objects.create(artwork=artwork, **image_data)
            
        return artwork

    def update(self, instance, validated_data):
        # Handle nested images
        images_data = validated_data.pop('images', None)
        
        # Update artwork fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update images if provided
        if images_data is not None:
            # Delete existing images
            instance.images.all().delete()
            
            # Create new images
            for image_data in images_data:
                ArtworkImage.objects.create(artwork=instance, **image_data)
        
        return instance

class ArtworkListSerializer(serializers.ModelSerializer):
    primary_image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.category_name', read_only=True)

    class Meta:
        model = Artwork
        fields = ('id', 'title', 'primary_image', 'category_name')

    def get_primary_image(self, obj):
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image_url
        return None 