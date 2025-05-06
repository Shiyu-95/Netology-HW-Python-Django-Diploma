from django.db import models
from django.contrib.auth import get_user_model
from geopy.geocoders import Nominatim

User = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.CharField(max_length=50)
    place = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=7, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.place:
            self.get_geocoordinates()
        super().save(*args, **kwargs)

    def get_geocoordinates(self):
        geolocator = Nominatim(user_agent="my_app")
        location = geolocator.geocode(self.place)
        if location:
            self.latitude = location.latitude
            self.longitude = location.longitude

    def get_place_name(self):
        geolocator = Nominatim(user_agent="my_app")
        location = geolocator.reverse(f"{self.latitude}, {self.longitude}")
        return location.address


class PostImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="post_images", null=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
