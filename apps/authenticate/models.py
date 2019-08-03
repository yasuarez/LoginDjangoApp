from django.db import models

# Create your models here.
from django.contrib.auth.models import User
# Create your models here.
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_birth = models.DateField(auto_now=False, auto_now_add=False)
    profile_image = models.ImageField(upload_to='profile_images',blank=True)

    class Meta:
        permissions = (
            ("download_pdf", "Puede descargar PDF"),
            ("permiso_1", "Custom Permiso 1"),
            ("permiso_2", "Custom Permiso 2"),
            ("permiso_3", "Custom Permiso 3"),
            ("permiso_4", "Custom Permiso 4"),
        )
    
    def __str__(self):
        return self.user.username

    def showMyProfilePicture(self):
        return self.profile_image.url