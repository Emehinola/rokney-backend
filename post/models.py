from django.db import models
from users_account.models import CustomUser

# Create your models here.

# model for images, videos uploads


# model for post from users


class Post(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    subtitle = models.CharField(max_length=10)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.content[:10]}..."

    class Meta:
        ordering = ['-time']

# for comments to all posts


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.CharField(max_length=250)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.content[:20]}"

    class Meta:
        ordering = ['-time']

# for likes to a post


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.user.username} - {self.post.content}"


# image uploads album


class FileAlbum(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    images = models.FileField(upload_to="post_images", blank=True)
    image_url = models.CharField(blank=True, max_length=300)

    def save(self, *args, **kwargs):
        self.image_url = self.images
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.images.url
