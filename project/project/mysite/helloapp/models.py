from django.db import models


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