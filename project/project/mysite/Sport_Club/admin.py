from django.contrib import admin
from .models import Students, Coach, Groups, ListTraining  # Змінено на ListTraining

# Реєстрація моделей в адмінці
admin.site.register(Students)
admin.site.register(Coach)
admin.site.register(Groups)
admin.site.register(ListTraining)  # Змінено на ListTraining
