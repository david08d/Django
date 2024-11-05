from django.db import models

class Groups(models.Model):
    group_name = models.CharField(max_length=88)
    coach = models.ForeignKey('Coach', on_delete=models.CASCADE)  # Зовнішній ключ до тренера
    type_of_training = models.CharField(max_length=88)
    description = models.TextField()

    def __str__(self):
        return self.group_name


class Coach(models.Model):
    name = models.CharField(max_length=88)
    surname = models.CharField(max_length=88)
    age = models.IntegerField()

    def __str__(self):
        return f'{self.name} {self.surname} ({self.age} років)'


class Students(models.Model):
    name = models.CharField(max_length=88)
    surname = models.CharField(max_length=88)
    age = models.IntegerField()
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)  # Зовнішній ключ до групи

    def __str__(self):
        return f'{self.name} {self.surname} ({self.age} років, група: {self.group})'


class ListTraining(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    type_of_training = models.CharField(max_length=88)
    time_date_and_week = models.DateTimeField()

    def __str__(self):
        return f'{self.type_of_training} для групи {self.group} о {self.time_date_and_week}'

