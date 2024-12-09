from django.db import models
from django.conf import settings


class AuthorMake(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} {self.surname}'


class Books(models.Model):
    title = models.CharField(max_length=100)
    year = models.IntegerField(max)
    author_make = models.ForeignKey(AuthorMake,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ({self.year}) by {self.author_make}'




class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(blank=True, upload_to='users/%Y%m%d/')
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
