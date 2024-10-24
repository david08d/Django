from django.db import models

class Students(models.Model):
    name_student = models.CharField(max_length=88)
    surname_student = models.CharField(max_length=88)
    age_student = models.IntegerField()
    group_name = models.IntegerField(on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name_student} {self.surname_student} {self.age_student}{self.group_name}'


class Coach(models.Model):
    name_couch = models.CharField(max_length=88)
    surname_couch = models.CharField(max_length=88)
    age_couch = models.IntegerField()
    groups = models.IntegerField()
    type_of_training = models.CharField(max_length=88)

    def __str__(self):
        return f'{self.name_couch} {self.surname_couch} {self.age_couch} {self.age_couch}{self.groups}{self.type_of_training}'

class Groups(models.Model):
    groups_name = models.CharField(max_length=88)
    name_couch = models.CharField(max_length=88)
    students_list = models.TextField(max_length=888)
    type_of_training = models.CharField(max_length=88)
    description = models.TextField(max_length=888)

class List_training(models.Model):
    type_of_training = Groups.type_of_training
    group = Groups.groups_name
    time_date_and_week = models.IntegerField()



