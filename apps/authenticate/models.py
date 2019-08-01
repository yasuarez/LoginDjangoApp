from django.db import models

# Create your models here.
from django.contrib.auth.models import User
# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_birth = models.DateField(auto_now=False, auto_now_add=False)
    profile_image = models.ImageField(upload_to='profile_images',blank=True)

    def __str__(self):
        return self.user.username