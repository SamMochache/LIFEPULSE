from django.contrib import admin
from .models import Vitals

@admin.register(Vitals)
class VitalsAdmin(admin.ModelAdmin):
    list_display = ('user', 'heart_rate', 'systolic_bp', 'diastolic_bp', 'blood_sugar', 'oxygen_saturation', 'temperature', 'date_recorded')
    list_filter = ('date_recorded', 'user')
    search_fields = ('user__username',)
