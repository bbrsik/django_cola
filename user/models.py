from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(null=True, blank=True)
    last_name = models.TextField(null=True, blank=True)
    middle_name = models.TextField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    current_location = models.TextField(null=True, blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to='profiles/', default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"USERNAME: {self.user}, "
            f"CREATED AT: {self.created_at}, "
            f"CURRENT LOCATION: {self.current_location}, "
            f"FIRST NAME: {self.first_name}, "
            f"LAST NAME: {self.last_name}, "
            f"MIDDLE NAME: {self.middle_name}, "
            f"BIRTHDATE: {self.birthdate}, "
            f"PROFILE PICTURE: {self.picture or None} "
        )
